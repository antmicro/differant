# Differant

A small library for diffing related codebases.

Uses a `.differant.yml` file in YAML to highlight expected differences.

Work in progress, use at your own risk.

## Usage

./differant.py DIRECTORY [--override]

Without the `--override` flag, if `DIRECTORY-upstream` and `DIRECTORY-derived` exist, the program skips the preparations phase and assumes the directories reflect the upstream and downstream code respectively. Using the flag deletes the directories first.

Differant assumes that you run it from outside the DIRECTORY.

By deault, it will perform a diff (taking into account the info from `.differant.yml`), print any diffs it cannot associate with a specific change listed in the conf file, and wait for changes of the conf file to re-run the diff (the point is to add to the conf file until you run out of ideas what he patches are about.

## TODO

* in [issues](https://github.com/antmicro/differant/issues)
