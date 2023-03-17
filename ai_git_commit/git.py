import os
import subprocess
from typing import Dict, List, Optional

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from ai_git_commit.config import ICommitMessage

DEFAULT_TYPE_OPTIONS = [
    {"value": "feat", "label": "✨ feat", "hint": "A new feature"},
    {"value": "fix", "label": "🐛 fix", "hint": "A bug fix"},
    {"value": "docs", "label": "📝 docs", "hint": "Documentation only changes"},
    {
        "value": "refactor",
        "label": "🔨 refactor",
        "hint": "A code change that neither fixes a bug nor adds a feature",
    },
    {
        "value": "perf",
        "label": "🚀 perf",
        "hint": "A code change that improves performance",
    },
    {
        "value": "test",
        "label": "🧪 test",
        "hint": "Adding missing tests or correcting existing tests",
    },
    {
        "value": "build",
        "label": "🏗️ build",
        "hint": "Changes that affect the build system or external dependencies",
    },
    {
        "value": "ci",
        "label": "🤖 CI",
        "hint": "Changes to our CI configuration files and scripts",
    },
]


def get_git_diff_output() -> str:
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    return result.stdout


def get_git_status_short_output() -> str:
    result = subprocess.run(
        ["git", "status", "--short"], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    return result.stdout


def git_user_commit_message() -> ICommitMessage:
    type_completer = WordCompleter([option["value"] for option in DEFAULT_TYPE_OPTIONS])
    selected_type = prompt(
        f"Select the commit type ({','.join(list(type_completer.words))}): ",
        completer=type_completer,
        complete_while_typing=True,
    )

    commit_type = next(
        (
            option["label"]
            for option in DEFAULT_TYPE_OPTIONS
            if option["value"] == selected_type
        ),
        None,
    )
    commit_subject = input(
        f"{commit_type}: "
        if commit_type
        else "Write a brief title description for commit: "
    )
    commit_messages = []
    while True:
        msg = input(" - ")
        if not msg:
            break
        commit_messages.append(msg)

    if commit_type:
        commit_subject = f"{commit_type}: {commit_subject}"

    return ICommitMessage(id=0, subject=commit_subject, body=commit_messages)


# def isInitGitRepository() -> bool:
#     pass


# def execGitCommit(commitMessage: Dict[str, Any]) -> str:
#     pass
