from files import blame_file


def test_blame_file(git_repo):
    path = git_repo.workspace
    file = path / 'test.txt'

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

    blob = git_repo.api.tree()["test.txt"]

    assert blame_file(git_repo.api, blob) == (3, [("Tony Stark <tony@avengers.com>", 2), ("Steve Rogers <captain@avengers.com>", 1)])


def test_blame_file_ignore_revs(git_repo):
    path = git_repo.workspace
    file = path / 'test.txt'

    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value("user", "email", "tony@avengers.com").release()
    file.write_text("test\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add file")

    git_repo.api.config_writer().set_value("user", "name", "Steve Rogers").release()
    git_repo.api.config_writer().set_value("user", "email", "captain@avengers.com").release()
    file.write_text("test\nanother\n")
    git_repo.api.index.add(file)
    commit = git_repo.api.index.commit("Add another line")

    git_repo.api.config_writer().set_value("user", "name", "Tony Stark").release()
    git_repo.api.config_writer().set_value("user", "email", "tony@avengers.com").release()
    file.write_text("test\nanother\nline\n")
    git_repo.api.index.add(file)
    git_repo.api.index.commit("Add another line")

    blob = git_repo.api.tree()["test.txt"]

    assert blame_file(git_repo.api, blob, ignore_revs=[str(commit)]) == (2, [('Tony Stark <tony@avengers.com>', 1), ('Steve Rogers <captain@avengers.com>', 1)])
