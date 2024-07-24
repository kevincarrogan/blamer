from files import blame_file


def blame_folder(repo, tree):
    total = 0
    user_totals = {}
    blobs = []
    for blob in tree.blobs:
        total_from_blob, aggregated_users_totals = blame_file(repo, blob)
        total += total_from_blob
        for user, user_total in aggregated_users_totals:
            user_totals.setdefault(user, 0)
            user_totals[user] += user_total
        blobs.append(
            (blob.name, (total_from_blob, aggregated_users_totals)),
        )

    return (total, list(user_totals.items()), blobs)
