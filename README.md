# Differant

Copyright (c) 2020-2022 [Antmicro](https://www.antmicro.com)

[![View on Antmicro Open Source Portal](https://img.shields.io/badge/View%20on-Antmicro%20Open%20Source%20Portal-332d37?style=flat-square)](https://opensource.antmicro.com/projects/differant)

A small library for diffing related codebases.

Uses a `.differant.yml` file in YAML to highlight expected differences.

Work in progress, use at your own risk.

## Usage

```
./differant.py DIRECTORY [--override]
```

Without the `--override` flag, if `DIRECTORY-upstream` and `DIRECTORY-derived` exist, the program skips the preparations phase and assumes the directories reflect the upstream and downstream code respectively. Using the flag deletes the directories first.

Differant assumes that you run it from outside the DIRECTORY.

By deault, it will perform a diff once (taking into account the info from `.differant.yml`), print any diffs it cannot associate with a specific change listed in the conf file.

If the `--interactive` flag is provided, the program will wait for changes of the conf file to re-run the diff (the point is to add to the conf file until you run out of ideas what he patches are about.

## Conf file

By default it's called `.differant.yml`. Currently it has the following sections:

* ignores - removes files (what) which differ but are not meanigful (thus eliminating lots of non-meaningful patches) with an explanation (why)
* refactors - strings which changed but simply replacing the 'from' string to a 'to' string solves a lot of patches
* known_changes - groups of files (in a files section) which implement related changes (changes)

## TODO

* in [issues](https://github.com/antmicro/differant/issues)

## Changelogs tool

The changelogs feature has for now been implemented as a separate file - `changelogs.py` - but metaphorically speaking it is solving a very similar problem to `differant`.

### Usage

Generate logs:

```
git log --pretty=format:"%C(yellow)%h%Creset | %C(cyan)%C(bold)%ad%Creset | %s" --date=format:'%Y-%m-%d,%H:%M:%S' > log_file
```

Run:

```
./changelogs.py parse-gitlogs log_file_1 log_file2 ... > changelog.yml
```

And then:

```
./changelogs.py print-changelog changelog.yml
```
