import argparse
import json
import pathlib

from git import Repo

from folders import blame_folder


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=pathlib.Path)
    args = parser.parse_args()

    repo = Repo(args.repo)

    output = blame_folder(repo, repo.tree())

    print(json.dumps(output))
