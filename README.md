# Differant

A small library for diffing related codebases.

Uses a `.differant.conf` file in HOCON to highlight expected differences.

Work in progress, use at your own risk.

## TODO

* [X] implement ignored files, preferably with explanations
* [X] put .differant.conf as into the ignored list by default
* [ ] implement moving files
* [ ] switch from deleting files to operation on diffs
  * [X] generate a diff file
  * [X] use python-unidiff to parse diff file
  * [X] mark and detect refactorizations and ignore/group them
  * [ ] categorize changes - refactors vs uncategorized, perhaps just as patchset metadata
  * [ ] find more obvious refactors
  * [ ] from uncategorized, sort them by amount of changes
  * [ ] generate a nice summary of it all
  * [ ] enable to generate subdiffs
  * [ ] explore if we can add metadata to diffs
  * [ ] find/write a good diff viewer
