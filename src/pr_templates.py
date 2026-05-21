import random


BRANCH_PREFIXES = (
    "feat",
    "fix",
    "chore",
    "refactor",
    "docs",
    "style",
    "perf",
)


TITLE_TEMPLATES = {
    "feat": (
        "feat: add {subject} helper",
        "feat: support {subject} option",
        "feat: introduce {subject} module",
        "feat: expose {subject} utility",
    ),
    "fix": (
        "fix: handle {subject} edge case",
        "fix: correct {subject} fallback",
        "fix: prevent {subject} race condition",
        "fix: resolve {subject} regression",
    ),
    "chore": (
        "chore: bump {subject} dependency",
        "chore: clean up {subject} references",
        "chore: tidy {subject} configuration",
        "chore: remove unused {subject} files",
    ),
    "refactor": (
        "refactor: extract {subject} into module",
        "refactor: simplify {subject} flow",
        "refactor: rename {subject} for clarity",
        "refactor: split {subject} responsibilities",
    ),
    "docs": (
        "docs: clarify {subject} usage",
        "docs: document {subject} behaviour",
        "docs: update {subject} examples",
        "docs: improve {subject} section",
    ),
    "style": (
        "style: format {subject} block",
        "style: normalize {subject} indentation",
        "style: tidy {subject} imports",
    ),
    "perf": (
        "perf: reduce {subject} allocations",
        "perf: cache {subject} lookups",
        "perf: avoid redundant {subject} calls",
    ),
}


BODY_TEMPLATES = (
    "Small adjustment around {subject}. No behavioural change expected.",
    "Minor follow-up that touches {subject}. Reviewed locally.",
    "Quick iteration on {subject}. Safe to land.",
    "Light pass over {subject}. Keeping the change self-contained.",
    "Routine update covering {subject}.",
)


SUBJECT_WORDS = (
    "config",
    "parser",
    "logger",
    "client",
    "handler",
    "validator",
    "serializer",
    "registry",
    "scheduler",
    "renderer",
    "adapter",
    "loader",
    "builder",
    "formatter",
    "resolver",
    "dispatcher",
    "cache",
    "queue",
    "session",
    "metadata",
)


def random_prefix():
    return random.choice(BRANCH_PREFIXES)


def random_subject():
    return random.choice(SUBJECT_WORDS)


def random_branch(prefix, subject):
    suffix = random.randint(1000, 9999)
    return f"{prefix}/{subject}-{suffix}"


def random_title(prefix, subject):
    return random.choice(TITLE_TEMPLATES[prefix]).format(subject=subject)


def random_body(subject):
    return random.choice(BODY_TEMPLATES).format(subject=subject)
