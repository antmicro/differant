#!/usr/bin/env python3

# for now assuming the 'derived' repo is just checked out

import fire, pyhocon, git, os, shutil, sys, pathlib, subprocess, unidiff

def dirdiff(directory, override=False):
    "Either a function to diff directories, or a city in Northwest England, close to Dirham and Dirwick."
    if not shutil.rmtree.avoids_symlink_attacks:
        print("Sorry, but your system is susceptible to symlink attacks. Consider switching. Exiting.")
        sys.exit(1)
    directory = directory.rstrip('/')
    abspath = os.path.abspath(directory)
    if abspath in pathlib.Path(os.getcwd()).parents or abspath == os.getcwd():
        print("Please do not call dirdiff from inside of the target directory.")
        sys.exit(1)
    configfile = directory + '/.differant.conf'
    conf = pyhocon.ConfigFactory.parse_file(configfile)
    print(conf)
    upstream = directory + '-upstream'
    derived = directory + '-derived'
    if override == True:
        shutil.rmtree(upstream)
        shutil.rmtree(derived)
    if not os.path.isdir(upstream):
        repo = git.Repo.clone_from(conf['upstream'], upstream, depth=1, branch=conf['tag'])
    else:
        print(f"Skipping clone, upstream directory {upstream} exists.")
    if not os.path.isdir(derived):
        shutil.copytree(directory, f'{directory}-derived')
    else:
        print(f"Skipping copy, derived directory {derived} exists.")
    shutil.rmtree(upstream+'/.differant.conf', ignore_errors=True)
    shutil.rmtree(derived+'/.differant.conf', ignore_errors=True)
    for i, reason in conf['ignore'].items():
        # this is only applicable to Linux!
        if i[0] == '/' or i.find('..') != -1:
            print(f'Nice try. Ignoring directory {i}, please do not use absolute paths and parent folders.')
            continue
        print(f"Removing {i}, reason: {reason}")
        shutil.rmtree(upstream+'/'+i, ignore_errors=True)
        shutil.rmtree(derived+'/'+i, ignore_errors=True)

    # let's diff the dirs now, and parse this into a Python patchset object
    result = subprocess.run(f"git diff --no-index {upstream} {derived}".split(' '), stdout=subprocess.PIPE)
    result_output = result.stdout.decode('utf-8')
    patchset = unidiff.PatchSet(result_output)
    for p in patchset:
        print(f"Patch with {p.added} added lines and {p.removed} removed lines")

if __name__ == '__main__':
    fire.Fire(dirdiff)
