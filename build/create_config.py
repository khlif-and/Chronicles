"""
GitHub Filler - Fake Commit Generator for GitHub

Copyright (C) 2024-2024 Liam Arguedas

This file is part of GitHub Filler, a free CLI tool based on the original Commitify
designed to generate fake commits for GitHub repositories.

GitHub Filler is distributed under the terms of the GNU General Public License (GPL),
either version 3 of the License, or any later version.

GitHub Filler is provided "as is", without warranty of any kind, express or implied,
including but not limited to the warranties of merchantability, fitness for a
particular purpose, and noninfringement. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
GitHub Filler. If not, see <https://www.gnu.org/licenses/>.
"""

from pathlib import Path
import json


BLANK = ""
CONFIG = "config.json"
AFFIRMATIVE_ANSWERS = {"y", "yes"}

DEFAULT_PR_COUNT = 5
DEFAULT_PR_MERGE_RATIO = 0.0
DEFAULT_PR_DELAY_MIN_SECONDS = 300
DEFAULT_PR_DELAY_MAX_SECONDS = 1800
DEFAULT_PR_WORKSPACE = "pr_workspace"


class GithubFillerConfig:
    """todo"""

    def __init__(self):
        self.cfg_dir = Path(__file__).parents[1] / "src" / "cfg"
        self.repository = None
        self.branch = "master"
        self.commits = ""
        self.file = "py"
        self.starting_date = str()
        self.ending_date = str()
        self.pr_enabled = False
        self.pr_count = DEFAULT_PR_COUNT
        self.pr_merge_ratio = DEFAULT_PR_MERGE_RATIO
        self.pr_delay_min_seconds = DEFAULT_PR_DELAY_MIN_SECONDS
        self.pr_delay_max_seconds = DEFAULT_PR_DELAY_MAX_SECONDS
        self.pr_workspace = DEFAULT_PR_WORKSPACE

    def declare_settings(self):
        """todo"""
        if self.repository == BLANK:
            print("Repository not detected, please reconfigure: ")
        return {
            "repository": self.repository,
            "branch": "master" if self.branch == BLANK else self.branch,
            "commits": self.commits,
            "file": "py" if self.file == BLANK else self.file,
            "starting_date": self.starting_date,
            "ending_date": self.ending_date,
            "pr_enabled": self.pr_enabled,
            "pr_count": self.pr_count,
            "pr_merge_ratio": self.pr_merge_ratio,
            "pr_delay_min_seconds": self.pr_delay_min_seconds,
            "pr_delay_max_seconds": self.pr_delay_max_seconds,
            "pr_workspace": self.pr_workspace,
        }

    def ask_configs(self, return_configs=False):
        """todo"""

        self.repository = input("Repository URL: ")
        self.branch = input("Branch (Default: master (RECOMENDED) ): ")
        self.commits = input(
            "Number of Daily commits (Default: Random (RECOMENDED) ): "
        )
        self.file = input("Commit File type (Default: py): ")
        print("Please follow date formating (year, month, day): Example: 2024, 1, 12")
        print("NOTE: No leading zeros.")
        self.starting_date = input("Enter starting date: ")
        self.ending_date = input("Enter ending date: ")

        self.ask_pr_configs()

        configs = self.declare_settings()

        self.save_configs(configs)

        print("SETTINGS: Loaded ----------- ")
        print(f'Repository: {configs["repository"]}')
        print(f'Branch: {configs["branch"]}')
        print(
            f'Commits: {"random" if configs["commits"] == BLANK else configs["commits"]}'
        )
        print(f'File: {configs["file"]}')
        print(f"Starting_date: {self.starting_date}")
        print(f"ending_date: {self.ending_date}")
        print(f"PR enabled: {configs['pr_enabled']}")
        if configs["pr_enabled"]:
            print(f"PR count: {configs['pr_count']}")
            print(f"PR merge ratio: {configs['pr_merge_ratio']}")
            print(
                "PR delay: "
                f"{configs['pr_delay_min_seconds']}s - "
                f"{configs['pr_delay_max_seconds']}s"
            )
            print(f"PR workspace: {configs['pr_workspace']}")

        print("-----------------------------")

        if return_configs:
            return configs

    def ask_pr_configs(self):
        print("--- Pull Request generation (optional) ---")
        answer = input("Generate PRs after commits? (y/N): ").strip().lower()
        self.pr_enabled = answer in AFFIRMATIVE_ANSWERS

        if not self.pr_enabled:
            return

        self.pr_count = self.read_int(
            f"Number of PRs (Default: {DEFAULT_PR_COUNT}): ",
            DEFAULT_PR_COUNT,
            minimum=1,
        )
        self.pr_merge_ratio = self.read_ratio(
            f"Merge ratio 0.0-1.0 (Default: {DEFAULT_PR_MERGE_RATIO}): ",
            DEFAULT_PR_MERGE_RATIO,
        )
        self.pr_delay_min_seconds = self.read_int(
            f"Min delay between PRs in seconds (Default: {DEFAULT_PR_DELAY_MIN_SECONDS}): ",
            DEFAULT_PR_DELAY_MIN_SECONDS,
            minimum=0,
        )
        self.pr_delay_max_seconds = self.read_int(
            f"Max delay between PRs in seconds (Default: {DEFAULT_PR_DELAY_MAX_SECONDS}): ",
            DEFAULT_PR_DELAY_MAX_SECONDS,
            minimum=self.pr_delay_min_seconds,
        )
        workspace_input = input(
            f"PR workspace folder (Default: {DEFAULT_PR_WORKSPACE}): "
        ).strip()
        self.pr_workspace = workspace_input or DEFAULT_PR_WORKSPACE

    @staticmethod
    def read_int(prompt, default, minimum=None):
        raw_value = input(prompt).strip()
        if raw_value == BLANK:
            return default
        try:
            parsed_value = int(raw_value)
        except ValueError:
            print(f"Invalid number, using default {default}")
            return default
        if minimum is not None and parsed_value < minimum:
            print(f"Value below minimum {minimum}, using {minimum}")
            return minimum
        return parsed_value

    @staticmethod
    def read_ratio(prompt, default):
        raw_value = input(prompt).strip()
        if raw_value == BLANK:
            return default
        try:
            parsed_value = float(raw_value)
        except ValueError:
            print(f"Invalid ratio, using default {default}")
            return default
        if parsed_value < 0.0 or parsed_value > 1.0:
            print(f"Ratio out of range, using default {default}")
            return default
        return parsed_value

    def save_configs(self, cfgs):
        """todo"""
        with open(self.cfg_dir / CONFIG, "w", encoding="utf-8") as file:
            json.dump(cfgs, file)
