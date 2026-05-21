import random
import subprocess
import time
from pathlib import Path

from .file_builder import FileBuilder
from .pr_templates import (
    random_body,
    random_branch,
    random_prefix,
    random_subject,
    random_title,
)


class PRBuilderError(Exception):
    pass


class PRBuilder:

    def __init__(
        self,
        workspace,
        repository,
        base_branch,
        merge_ratio,
        delay_min_seconds,
        delay_max_seconds,
    ):
        self.workspace = Path(workspace)
        self.repository = repository
        self.base_branch = base_branch
        self.merge_ratio = merge_ratio
        self.delay_min_seconds = delay_min_seconds
        self.delay_max_seconds = delay_max_seconds
        self.file_generator = FileBuilder()

    def run(self, pr_count):
        self.ensure_dependencies()
        self.prepare_workspace()

        merged_count = 0
        opened_count = 0
        failed_count = 0

        for index in range(pr_count):
            print(f"--- PR {index + 1}/{pr_count} ---")
            try:
                was_merged = self.create_single_pr()
                if was_merged:
                    merged_count += 1
                else:
                    opened_count += 1
            except PRBuilderError as error:
                failed_count += 1
                print(f"PR failed: {error}")

            if index < pr_count - 1:
                self.sleep_random()

        print("--- PR generation summary ---")
        print(f"Merged: {merged_count}")
        print(f"Open:   {opened_count}")
        print(f"Failed: {failed_count}")

    def ensure_dependencies(self):
        for binary in ("git", "gh"):
            if not self.command_available(binary):
                raise PRBuilderError(f"{binary} is not available on PATH")

    def prepare_workspace(self):
        if self.workspace.exists() and (self.workspace / ".git").exists():
            self.run_command(["git", "fetch", "origin"], cwd=self.workspace)
            self.run_command(
                ["git", "checkout", self.base_branch], cwd=self.workspace
            )
            self.run_command(
                ["git", "pull", "origin", self.base_branch], cwd=self.workspace
            )
            return

        self.workspace.parent.mkdir(parents=True, exist_ok=True)
        self.run_command(
            ["git", "clone", self.repository, str(self.workspace)],
            cwd=self.workspace.parent,
        )

    def create_single_pr(self):
        prefix = random_prefix()
        subject = random_subject()
        branch_name = random_branch(prefix, subject)
        title = random_title(prefix, subject)
        body = random_body(subject)

        self.sync_base()
        self.create_branch(branch_name)
        self.apply_dummy_change()
        self.commit_change(title)
        self.push_branch(branch_name)
        self.open_pull_request(title, body, branch_name)

        should_merge = random.random() < self.merge_ratio
        if should_merge:
            self.merge_pull_request(branch_name)

        self.return_to_base()
        return should_merge

    def sync_base(self):
        self.run_command(
            ["git", "checkout", self.base_branch], cwd=self.workspace
        )
        self.run_command(
            ["git", "pull", "origin", self.base_branch], cwd=self.workspace
        )

    def create_branch(self, branch_name):
        self.run_command(
            ["git", "checkout", "-b", branch_name], cwd=self.workspace
        )

    def apply_dummy_change(self):
        self.file_generator.create_file(self.workspace)

    def commit_change(self, title):
        self.run_command(["git", "add", "."], cwd=self.workspace)
        self.run_command(
            ["git", "commit", "-m", title], cwd=self.workspace
        )

    def push_branch(self, branch_name):
        self.run_command(
            ["git", "push", "-u", "origin", branch_name], cwd=self.workspace
        )

    def open_pull_request(self, title, body, branch_name):
        self.run_command(
            [
                "gh",
                "pr",
                "create",
                "--base",
                self.base_branch,
                "--head",
                branch_name,
                "--title",
                title,
                "--body",
                body,
            ],
            cwd=self.workspace,
        )

    def merge_pull_request(self, branch_name):
        self.run_command(
            [
                "gh",
                "pr",
                "merge",
                branch_name,
                "--squash",
                "--delete-branch",
            ],
            cwd=self.workspace,
        )

    def return_to_base(self):
        self.run_command(
            ["git", "checkout", self.base_branch], cwd=self.workspace
        )

    def sleep_random(self):
        wait_seconds = random.randint(
            self.delay_min_seconds, self.delay_max_seconds
        )
        minutes = round(wait_seconds / 60, 1)
        print(f"Waiting {wait_seconds}s (~{minutes} min) before next PR")
        time.sleep(wait_seconds)

    @staticmethod
    def command_available(binary):
        try:
            subprocess.run(
                [binary, "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    @staticmethod
    def run_command(arguments, cwd):
        result = subprocess.run(
            arguments,
            cwd=str(cwd),
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            command_text = " ".join(arguments)
            error_output = result.stderr.strip() or result.stdout.strip()
            raise PRBuilderError(
                f"Command failed: {command_text}\n{error_output}"
            )
        return result.stdout
