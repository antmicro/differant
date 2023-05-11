#!/usr/bin/python3
import os
import fire
import git
import pdb
from pathlib import Path

class GitHelper(object):

    def log(self, dir='.', commit_from='HEAD~30', commit_to='HEAD'):
        """ Log commits recursively

        Logs commits recursively going into submodules
        """
        repo = git.Repo(dir)
        self._log_range(repo, commit_from, commit_to, name=Path(dir).absolute().name)

    def _log_range(self, repo, commit_from, commit_to, level=0, name=''):
        commits = list(repo.iter_commits('{}..{}'.format(commit_from if commit_from else '', commit_to)))

        for commit in commits:
            self._log_commit(name, commit, level)

    def _log_commit(self, name, commit, level=0):
        commit_message = commit.message.splitlines()[0].replace("\"", "\'")
        print(f"  - \"{Path(name).absolute().name} @ {commit.hexsha[:8]} {commit_message}\"")
        submodules = [x for x in commit.diff(next(commit.iter_parents())) if os.path.isdir(os.path.join(commit.repo.working_dir, x.a_path))]
        for subm in submodules:
            subrepo = git.Repo(os.path.join(commit.repo.working_dir, subm.a_path))
            self._log_range(subrepo, subm.b_blob, subm.a_blob, level=level+1, name=subm.a_path)

if __name__ == '__main__':
    fire.Fire(GitHelper)
