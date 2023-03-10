import subprocess, os
from typing import Dict, Any


def getGitDiffOutput() -> str:
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.stderr)
    return result.stdout


# def isInitGitRepository() -> bool:
#     pass


# def execGitCommit(commitMessage: Dict[str, Any]) -> str:
#     pass
