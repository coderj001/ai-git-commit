from ai_git_commit.git import getGitDiffOutput


def main():
    git_output = getGitDiffOutput()
    print(git_output)


if __name__ == "__main__":
    main()
