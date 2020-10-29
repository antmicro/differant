# Differant

A small library for diffing related codebases.

Uses a `.differant.yml` file in YAML to highlight expected differences.

Work in progress, use at your own risk.

## Usage

```
./differant.py DIRECTORY [--override]
```

Without the `--override` flag, if `DIRECTORY-upstream` and `DIRECTORY-derived` exist, the program skips the preparations phase and assumes the directories reflect the upstream and downstream code respectively. Using the flag deletes the directories first.

Differant assumes that you run it from outside the DIRECTORY.

By deault, it will perform a diff (taking into account the info from `.differant.yml`), print any diffs it cannot associate with a specific change listed in the conf file, and wait for changes of the conf file to re-run the diff (the point is to add to the conf file until you run out of ideas what he patches are about.

## Conf file

By default it's called `.differant.yml`. Currently it has the following sections:

* ignores - removes files (what) which differ but are not meanigful (thus eliminating lots of non-meaningful patches) with an explanation (why)
* refactors - strings which changed but simply replacing the 'from' string to a 'to' string solves a lot of patches
* known_changes - groups of files (in a files section) which implement related changes (changes)

## TODO

* in [issues](https://github.com/antmicro/differant/issues)
