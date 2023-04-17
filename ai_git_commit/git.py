import subprocess
import sys

from prompt_toolkit import HTML, PromptSession, print_formatted_text, prompt
from prompt_toolkit.completion import Completion, WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments_markdown_lexer.lexer import MarkdownLexer

from ai_git_commit.config import ICommitMessage


def git_user_commit_message() -> ICommitMessage:
    """
    The git_user_commit_message function is a function that prompts the user to enter a commit message.
    The function uses prompt_toolkit to create an interactive command line interface for the user.
    The first prompt asks the user to select from one of several options, each with their own label and hint text.
    Once selected, this option is used as part of the commit subject (e.g., "feat: Add new feature"). The second prompt asks
    the user for a brief description of what they are committing (e.g., "Add new feature"). Finally, there is an optional
    prompt where users can add more detailed information about their changes in markdown format.

    :return: A icommitmessage object.

    :doc-author: coderj001
    """
    style = Style.from_dict(
        {
            "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            "scrollbar.background": "bg:#88aaaa",
            "scrollbar.button": "bg:#222222",
        }
    )

    type_options = [
        {"value": "feat", "label": "✨ Features", "hint": "A new feature"},
        {"value": "fix", "label": "🐞 Bug Fixes", "hint": "A bug fix"},
        {
            "value": "docs",
            "label": "📝 Documentation",
            "hint": "Documentation only changes",
        },
        {
            "value": "style",
            "label": "💄 Styles",
            "hint": "Changes related to code styling, formatting, or linting",
        },
        {
            "value": "refactor",
            "label": "♻️ Code Refactoring",
            "hint": "Code refactoring or restructuring without changing the external behavior",
        },
        {"value": "test", "label": "🧪 Tests", "hint": "Adding or updating tests"},
        {
            "value": "chore",
            "label": "🔧 Maintenance",
            "hint": "Maintenance tasks or non-code related changes",
        },
        {
            "value": "perf",
            "label": "🚀 Performance",
            "hint": "Performance improvements or optimizations",
        },
        {
            "value": "security",
            "label": "🔒 Security",
            "hint": "Fixes or enhancements related to security vulnerabilities",
        },
        {
            "value": "ci",
            "label": "🤖 CI",
            "hint": "Changes related to Continuous Integration (CI) configuration or scripts",
        },
        {
            "value": "i18n",
            "label": "🌍 Internationalization",
            "hint": "Internationalization and localization updates",
        },
        {
            "value": "ui",
            "label": "🖌️ User Interface",
            "hint": "User Interface (UI) changes or enhancements",
        },
        {
            "value": "ux",
            "label": "👍 User Experience",
            "hint": "User Experience (UX) improvements or updates",
        },
        {
            "value": "build",
            "label": "🏗️ Build",
            "hint": "Changes related to build systems or dependencies",
        },
        {
            "value": "config",
            "label": "⚙️ Configuration",
            "hint": "Configuration updates or changes",
        },
        {
            "value": "deps",
            "label": "📦 Dependencies",
            "hint": "Dependency updates or changes",
        },
        {
            "value": "revert",
            "label": "↩️ Revert",
            "hint": "Reverting a previous commit or change",
        },
        {
            "value": "lint",
            "label": "🔍 Linting",
            "hint": "Linting-related updates or improvements",
        },
        {
            "value": "release",
            "label": "🚀 Release",
            "hint": "Commits related to a new release or version",
        },
        {
            "value": "infra",
            "label": "🖥️ Infrastructure",
            "hint": "Infrastructure updates or changes, such as server configurations",
        },
        {
            "value": "animations",
            "label": "🎬 Animations",
            "hint": "Changes related to animations or transitions",
        },
        {
            "value": "examples",
            "label": "📚 Examples",
            "hint": "Updates or additions to example projects or code samples",
        },
        {
            "value": "logging",
            "label": "🔍 Logging",
            "hint": "Logging-related changes or improvements",
        },
        {
            "value": "monitoring",
            "label": "🔬 Monitoring",
            "hint": "Updates or additions to monitoring tools and configurations",
        },
    ]

    type_completer = WordCompleter([option["value"] for option in type_options])
    prompt_session = PromptSession(
        completer=type_completer, style=style, lexer=PygmentsLexer(MarkdownLexer)
    )

    def get_completions(document, complete_event):
        """
        The get_completions function is called when the user presses TAB.
        It should return a list of completions, each completion being a Completion object.
        The Completion object has three attributes: text, start_position and display_meta.
        text is the actual text that will be inserted into the document if this completion is selected by the user.
        start_position indicates where in the document to insert this completion (0 means right after current word).
        display_meta can be used to show extra information about this option in your UI.

        :param document: Used to Get the word before the cursor.
        :param complete_event: Used to Get the current line and column of the cursor.
        :return: A generator.

        :doc-author: coderj001
        """
        word_before_cursor = document.get_word_before_cursor()
        for option in type_options:
            if option["value"].startswith(word_before_cursor):
                yield Completion(
                    option["value"],
                    start_position=-len(word_before_cursor),
                    display=option["value"],
                    display_meta=option["hint"],
                )

    prompt_session.completer.get_completions = get_completions

    selected_type = prompt_session.prompt(
        HTML(
            "<b>Select the commit type <style fg='ansiwhite' bg='#00ff44'>[TAB]</style>:</b> "
        )
    )

    commit_type = next(
        (
            option["label"]
            for option in type_options
            if option["value"] == selected_type
        ),
        None,
    )

    prompt_session = PromptSession(
        style=style,
        lexer=PygmentsLexer(MarkdownLexer),
    )

    commit_subject = prompt_session.prompt(
        HTML(f"<style fg='ansiwhite' bg='#00ff44'>{commit_type}:</style> ")
        if commit_type
        else "Write a brief title description for commit: "
    )

    commit_messages = []
    print_formatted_text(
        HTML("<ansiblue>Description [ENTER to exit or skip]</ansiblue>")
    )
    while True:
        msg = prompt_session.prompt(" - ")
        if not msg:
            break
        commit_messages.append(msg)

    if commit_type:
        commit_subject = f"{commit_type}: {commit_subject}"

    return ICommitMessage(id=0, subject=commit_subject, body=commit_messages)


def get_git_diff_output() -> str:
    """
    The get_git_diff_output function returns the output of a git diff --staged command.

    The function uses subprocess to run the git diff --staged command and capture its output. If the return code is not 0,
    the function raises a CalledProcessError with an error message from stderr. Otherwise, it returns stdout as a string.

    :return: The output of the git diff --staged command.

    :doc-author: coderj001
    """
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    return result.stdout


def is_init_git_repository() -> bool:
    """
    The is_init_git_repository function checks if the current directory is a git repository.
    It does this by calling the `git rev-parse --is-inside-work-tree` command and checking its output.
    If it returns 0, then we are in a git repository; otherwise, we are not.

    :return: True if the current directory is a git repository.

    :doc-author: coderj001
    """
    try:
        subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False


def exec_git_commit(commitMessage: ICommitMessage) -> None:
    """
    The exec_git_commit function takes a commit message as an argument and writes it to the COMMIT_EDITMSG file.
    It then executes the git commit command with the -F flag, which tells git to use that file as its commit message.

    :param commitMessage:ICommitMessage: Used to Specify the type of the parameter.
    :return: Nothing.

    :doc-author: coderj001
    """
    with open("./.git/COMMIT_EDITMSG", "w") as f:
        f.write(f"{commitMessage['subject']}\n\n")
        for i in commitMessage["body"]:
            f.write(f" - {i}\n")

    subprocess.check_output(["git", "commit", "-F", "./.git/COMMIT_EDITMSG"])


def get_git_status_short_output() -> None:
    """
    The get_git_status_short_output function runs the git status command with the --short and --untracked-files=no flags.
    The output is printed to stdout in a green color.

    :return: The following:.

    :doc-author: coderj001
    """
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=no"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    print_formatted_text(
        HTML(
            f"<style fg='ansiwhite' bg='#00ff44'><b>Checking Git Status</b></style>\n<style fg='#42f566'>{result.stdout}</style>"
        )
    )


def run_command_git_commit() -> None:
    """
    The run_command_git_commit function is used to commit the changes in the current directory.
        It first checks if there is a git repository initialized in the current directory, and then it gets
        all of the files that have been modified or added since last commit. Then it asks for a user inputted
        message to be used as a commit message, and finally commits all of those changes with that message.

    :return: None.

    :doc-author: coderj001
    """
    if is_init_git_repository():
        get_git_status_short_output()
        commit_message = git_user_commit_message()

        checked = prompt(HTML("<b>Want to continue?</b> [y/n]: ")).lower()
        if checked.startswith("y") or checked == "":
            exec_git_commit(commit_message)
        else:
            print_formatted_text(
                HTML(
                    "<style fg='ansiwhite' bg='#ff0000'><b>Aborted:</b></style> canceled the commit ."
                )
            )
    else:
        print_formatted_text(
            HTML(
                "<style fg='ansiwhite' bg='#ff0000'><b>Error:</b></style> Current directory is not a git repository."
            )
        )

        sys.exit(1)
