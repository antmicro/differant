#!/usr/bin/env python3

# for now assuming the 'derived' repo is just checked out

import fire, yaml, git, os, shutil, sys, pathlib, subprocess, unidiff, time, logging

from neotermcolor import colored

def bold_yellow(text):
    return colored(text, color='yellow', attrs='bold')

conf_file = ".differant.yml"

def dirdiff(directory: str):
    "Either a function to diff directories, or a city in Wales, close to Dirham and Dirwick."

    f = open(f'{directory}/{conf_file}', 'r')
    conf = yaml.safe_load(f)
    f.close()

    upstream = directory + '-upstream'
    derived = directory + '-derived'

    if not os.path.isdir(upstream):
        repo = git.Repo.clone_from(conf['upstream'], upstream, depth=1, branch=conf['tag'])
    else:
        print(f"Skipping clone, upstream directory {upstream} exists.")

    if not os.path.isdir(derived):
        shutil.copytree(directory, derived)
    else:
        print(f"Skipping copy, derived directory {derived} exists.")

    for path in [conf_file, '.git']:
        shutil.rmtree(upstream+'/'+path, ignore_errors=True)
        shutil.rmtree(derived+'/'+path, ignore_errors=True)

    for i in conf['ignores']:
        what, why = i['what'], i['why']
        # this is only applicable to Linux!
        if os.path.isabs(what) or what.find('..') != -1:
            print(f'Nice try. Ignoring directory {what}, please do not use absolute paths and parent folders.')
            continue
        print(f"Removing {what}, reason: {why}")
        shutil.rmtree(upstream+'/'+what, ignore_errors=True)
        shutil.rmtree(derived+'/'+what, ignore_errors=True)

    # let's diff the dirs now, and parse this into a Python patchset object
    result = subprocess.run(f"git diff --no-index {upstream} {derived}".split(' '), stdout=subprocess.PIPE)
    result_output = result.stdout.decode('utf-8')
    patchset = unidiff.PatchSet(result_output)

    refactors = conf['refactors']

    for p in patchset:
        p.refactors = set()
        p.only_refactors = False
        if p.added == 0 and p.removed == 0:
            print("Empty patch:")
            print(p)
        elif check_if_refactor(p, refactors):
            print("Patch which only includes known refactors.")
            p.refactors = [dict(x) for x in p.refactors]
        else:
            print(f"Patch with {p.added} added lines and {p.removed} removed lines")
            for hunk in p:
                print("Added:")
                for line in [x for x in hunk if x.line_type == unidiff.LINE_TYPE_ADDED]:
                    print(line.value.rstrip())
                print("Removed:")
                for line in [x for x in hunk if x.line_type == unidiff.LINE_TYPE_REMOVED]:
                    print(line.value.rstrip())

    def get_size(patch):
        return patch.added + patch.removed

    l = sorted(patchset, key=get_size, reverse=True)

    for p in l:
        print(p.only_refactors, p.refactors, p.added, p.removed)


def check_if_refactor(patch, refactors):
    for hunk in patch:
        added = "".join([str(x)[1:] for x in hunk if x.line_type == unidiff.LINE_TYPE_ADDED])
        removed = "".join([str(x)[1:] for x in hunk if x.line_type == unidiff.LINE_TYPE_REMOVED])
        after_refactor = removed
        for r in refactors:
            was_added = False
            r_from, r_to = r['from'], r['to']
            if after_refactor.find(r_from) != -1:
                patch.refactors.add(tuple(r.items()))
                after_refactor = after_refactor.replace(r_from, r_to)
        if added == after_refactor:
            print("Lines equal after applying refactors.")
        else:
            return False
    patch.only_refactors = True
    return True

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class DiffingHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
    def on_modified(self, event):
        if event.src_path == f"{self.directory}/{conf_file}":
            print(bold_yellow('Change in {conf_file} detected, rerunning dirdiff again!'))
            dirdiff(self.directory)
            print(bold_yellow('Continuing to watch for changes...'))

def watch(directory: str, override: bool = False):

    if not shutil.rmtree.avoids_symlink_attacks:
        print("Sorry, but your system is susceptible to symlink attacks. Consider switching. Exiting.")
        sys.exit(1)

    directory = directory.rstrip('/')
    abspath = os.path.abspath(directory)
    if abspath in pathlib.Path(os.getcwd()).parents or abspath == os.getcwd():
        print("Please do not call dirdiff from inside of the target directory.")
        sys.exit(1)

    upstream = directory + '-upstream'
    derived = directory + '-derived'

    if override == True:
        shutil.rmtree(upstream)
        shutil.rmtree(derived)

    print(bold_yellow('Running dirdiff.'))
    dirdiff(directory)
    print(f'Starting to watch {bold_yellow(directory+"/"+conf_file)} for changes...')
    observer = Observer()
    observer.schedule(DiffingHandler(directory), path=directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":

    fire.Fire(watch)
