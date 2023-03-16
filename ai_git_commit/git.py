import os
import subprocess
from typing import Dict, List

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

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
        "label": "🤖 ci",
        "hint": "Changes to our CI configuration files and scripts",
    },
]


def get_git_diff_output() -> str:
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    return result.stdout


def git_user_commit_message() -> str:
    values_list: List[str] = [option["value"] for option in DEFAULT_TYPE_OPTIONS]
    type_completer = WordCompleter(values_list)

    selected_type = prompt(
        f"Select the type ({','.join(values_list)}): ",
        completer=type_completer,
        complete_while_typing=True,
    )

    commit_type = None
    commit_subject = None
    commit_message: List[str] = []
    for option in DEFAULT_TYPE_OPTIONS:
        if option["value"] == selected_type:
            commit_type = option["label"]
            break
    print("Write a brief subject for commit message:")
    if commit_type is not None:
        print(f"{commit_type}: ", end=" ")
    commit_subject = input()

    print("Enter a message for commit body (empty message to exit):")
    while True:
        msg = input(" - ")
        if not msg:
            break
        commit_message.append(msg)
    new_line = "" if len(commit_message) == 0 else "\n"
    if commit_type is None:
        return f"{commit_subject}{new_line}{new_line.join(commit_message)}"
    else:
        return (
            f"{commit_type}: {commit_subject}{new_line}{new_line.join(commit_message)}"
        )


# def isInitGitRepository() -> bool:
#     pass


# def execGitCommit(commitMessage: Dict[str, Any]) -> str:
#     pass
