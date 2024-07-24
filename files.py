def format_author(author):
    return f"{author.name} <{author.email}>"


def blame_file(repo, blob):
    blame = repo.blame(file=blob.path, rev=None)
    total = 0
    committers = {}

    for commit, lines in blame:
        total += len(lines)
        formatted_author = format_author(commit.author)
        committers.setdefault(format_author(commit.author), 0)
        committers[formatted_author] += len(lines)

    return (total, list(committers.items()))
