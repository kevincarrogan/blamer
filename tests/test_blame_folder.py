from folders import blame_folder


def test_blame_folder(git_repo):
    path = git_repo.workspace
    folder = path / "folder"
    folder.mkdir()
    file = folder / "test.txt"

    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value("user", "email", "tony@avengers.com").release()
    file.write_text("test\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add file")

    git_repo.api.config_writer().set_value("user", "name", "Steve Rogers").release()
    git_repo.api.config_writer().set_value("user", "email", "captain@avengers.com").release()
    file.write_text("test\nanother\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add another line")

    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value("user", "email", "tony@avengers.com").release()
    file.write_text("test\nanother\nline\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add another line")

    tree = git_repo.api.tree()["folder"]

    assert blame_folder(git_repo.api, tree) == (
        3,
        [("Tony Stark <tony@avengers.com>", 2), ("Steve Rogers <captain@avengers.com>", 1)],
        [
            ("test.txt", (3, [("Tony Stark <tony@avengers.com>", 2), ("Steve Rogers <captain@avengers.com>", 1)])),
        ],
    )
