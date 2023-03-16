import os
import subprocess
from typing import Any, Dict


def get_git_diff_output() -> str:
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    return result.stdout


# def isInitGitRepository() -> bool:
#     pass


# def execGitCommit(commitMessage: Dict[str, Any]) -> str:
#     pass
