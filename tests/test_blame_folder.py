from folders import blame_folder


def test_blame_folder(git_repo):
    path = git_repo.workspace
    folder = path / "folder"
    folder.mkdir()
    file = folder / "test.txt"

    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "tony@avengers.com"
    ).release()
    file.write_text("test\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add file")

    git_repo.api.config_writer().set_value("user", "name", "Steve Rogers").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "captain@avengers.com"
    ).release()
    file.write_text("test\nanother\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add another line")

    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "tony@avengers.com"
    ).release()
    file.write_text("test\nanother\nline\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add another line")

    tree = git_repo.api.tree()["folder"]

    assert blame_folder(git_repo.api, tree) == (
        "folder",
        3,
        [
            ("Tony Stark <tony@avengers.com>", 2),
            ("Steve Rogers <captain@avengers.com>", 1),
        ],
        [
            (
                "test.txt",
                3,
                [
                    ("Tony Stark <tony@avengers.com>", 2),
                    ("Steve Rogers <captain@avengers.com>", 1),
                ],
            ),
        ],
    )


def test_blame_folder_with_sub_folders(git_repo):
    path = git_repo.workspace
    folder = path / "folder"
    folder.mkdir()
    top_file = folder / "top.txt"
    top_file.write_text("test\n")
    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "tony@avengers.com"
    ).release()
    git_repo.api.index.add(top_file)
    git_repo.api.index.commit("Add file")

    sub_folder = folder / "sub_folder"
    sub_folder.mkdir()
    bottom_file = sub_folder / "bottom.txt"
    bottom_file.write_text("test\n")
    git_repo.api.config_writer().set_value("user", "name", "Steve Rogers").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "captain@avengers.com"
    ).release()
    git_repo.api.index.add(bottom_file)
    git_repo.api.index.commit("Add another file")

    tree = git_repo.api.tree()["folder"]

    assert blame_folder(git_repo.api, tree) == (
        "folder",
        2,
        [
            ("Steve Rogers <captain@avengers.com>", 1),
            ("Tony Stark <tony@avengers.com>", 1),
        ],
        [
            (
                "sub_folder",
                1,
                [("Steve Rogers <captain@avengers.com>", 1)],
                [("bottom.txt", 1, [("Steve Rogers <captain@avengers.com>", 1)])],
            ),
            ("top.txt", 1, [("Tony Stark <tony@avengers.com>", 1)]),
        ],
    )


def test_blame_folder_ignore_revs(git_repo):
    path = git_repo.workspace
    folder = path / "folder"
    folder.mkdir()
    file = folder / "test.txt"

    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "tony@avengers.com"
    ).release()
    file.write_text("test\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add file")

    git_repo.api.config_writer().set_value("user", "name", "Steve Rogers").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "captain@avengers.com"
    ).release()
    file.write_text("test\nanother\n")
    git_repo.api.index.add(file)
    commit = git_repo.api.index.commit("Add another line")

    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "tony@avengers.com"
    ).release()
    file.write_text("test\nanother\nline\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add another line")

    tree = git_repo.api.tree()["folder"]

    assert blame_folder(git_repo.api, tree, ignore_revs=[str(commit)]) == (
        "folder",
        2,
        [
            ("Tony Stark <tony@avengers.com>", 1),
            ("Steve Rogers <captain@avengers.com>", 1),
        ],
        [
            (
                "test.txt",
                2,
                [
                    ("Tony Stark <tony@avengers.com>", 1),
                    ("Steve Rogers <captain@avengers.com>", 1),
                ],
            )
        ],
    )


def test_blame_folder_with_sub_folders_ignore_revs(git_repo):
    path = git_repo.workspace
    folder = path / "folder"
    folder.mkdir()
    top_file = folder / "top.txt"
    top_file.write_text("test\n")
    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "tony@avengers.com"
    ).release()
    git_repo.api.index.add(top_file)
    git_repo.api.index.commit("Add file")

    sub_folder = folder / "sub_folder"
    sub_folder.mkdir()
    bottom_file = sub_folder / "bottom.txt"
    bottom_file.write_text("test\n")
    git_repo.api.config_writer().set_value("user", "name", "Steve Rogers").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "captain@avengers.com"
    ).release()
    git_repo.api.index.add(bottom_file)
    git_repo.api.index.commit("Add another file")

    top_file.write_text("test\nanother line\n")
    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value(
        "user", "email", "tony@avengers.com"
    ).release()
    git_repo.api.index.add(top_file)
    commit = git_repo.api.index.commit("Add another line")

    tree = git_repo.api.tree()["folder"]

    assert blame_folder(git_repo.api, tree, ignore_revs=[str(commit)]) == (
        "folder",
        3,
        [
            ("Steve Rogers <captain@avengers.com>", 1),
            ("Tony Stark <tony@avengers.com>", 2),
        ],
        [
            (
                "sub_folder",
                1,
                [("Steve Rogers <captain@avengers.com>", 1)],
                [("bottom.txt", 1, [("Steve Rogers <captain@avengers.com>", 1)])],
            ),
            ("top.txt", 2, [("Tony Stark <tony@avengers.com>", 2)]),
        ],
    )
