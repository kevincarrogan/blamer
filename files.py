from typing import Optional

from git import Repo
from git.objects.blob import Blob
from git.objects.commit import Commit
from git.util import Actor


def format_author(author: Actor) -> str:
    return f"{author.name} <{author.email}>"


def blame_file(repo: Repo, blob: Blob, *, ignore_revs: Optional[list[str]]=None) -> tuple[int, list[tuple[str, int]]]:
    if not ignore_revs:
        ignore_revs = []
    blame = repo.blame(file=str(blob.path), rev=None, rev_opts=ignore_revs)
    total = 0
    committers = {}

    for commit, lines, *_ in blame:
        total += len(lines)
        formatted_author = format_author(commit.author)
        committers.setdefault(format_author(commit.author), 0)
        committers[formatted_author] += len(lines)

    return (total, list(committers.items()))
