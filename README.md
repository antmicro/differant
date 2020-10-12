# Differant

A small library for diffing related codebases.

Uses a `.differant.conf` file in HOCON to highlight expected differences.

Work in progress, use at your own risk.

## TODO

* [X] implement ignored files, preferably with explanations
* [X] put .differant.conf as into the ignored list by default
* [ ] implement moving files
* [ ] switch from deleting files to operation on diffs
  * [ ] generate a diff file
  * [ ] use python-unidiff to parse diff file
  * [ ] use it to find most obvious changes that should be ignored and add to ignore list
  * [ ] find how many files only have a one-liner change
  * [ ] mark and detect refactorizations and ignore/group them
  * [ ] categorize changes
  * [ ] generate a nice summary of it all
