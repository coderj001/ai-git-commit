import subprocess
from unittest.mock import MagicMock, patch

from ai_git_commit.git import getGitDiffOutput


# TODO: Some Explanation require use ChatGPT and Google Search before moving forward.
def test_getGitDiffOutput_valid():
    expected_output = "file1.py\nfile2.py\n"
    # Mock the subprocess.run() function to return the expected output
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = expected_output
        mock_run.return_value = mock_result
        # Call the function and check that it returns the expected output
        output = getGitDiffOutput()
        assert output == expected_output
        # Check that subprocess.run() was called with the correct arguments
        mock_run.assert_called_once_with(
            ["git", "diff", "--staged"], capture_output=True, text=True
        )


def test_getGitDiffOutput_invalid():
    # Mock the subprocess.run() function to raise a CalledProcessError
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "error: failed to execute git diff command"
        mock_run.return_value = mock_result
        # Call the function and check that it raises a CalledProcessError
        try:
            getGitDiffOutput()
            # The function should raise an error, so the test should fail if it gets to this point
            assert False
        except subprocess.CalledProcessError as e:
            assert e.returncode == 1
        # Check that subprocess.run() was called with the correct arguments
        mock_run.assert_called_once_with(
            ["git", "diff", "--staged"], capture_output=True, text=True
        )
