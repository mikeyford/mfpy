from IPython.display import clear_output
import os
import git


def iter_update(i, max, update_n=10):
    """Pretty prints u"""
    if i % update_n == 0:
        done_pc = 100*i/max
        clear_output(wait=True)
        print(round(done_pc, 1), "% done.", sep="")


def pprint(string):
    """Prints update string after clearing cell output"""
    clear_output(wait=True)
    print(string)

    
def git_root(path):
    "Wraps local path in full path using git root"
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return os.path.join(git_root, path)


