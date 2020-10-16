# Differant

## TODO

* [X] implement ignored files, preferably with explanations
* [X] put .differant.conf as into the ignored list by default
* [ ] implement moving files
* [ ] switch from deleting files to operation on diffs
  * [X] generate a diff file
  * [X] use python-unidiff to parse diff file
  * [ ] use it to find most obvious changes that should be ignored and add to ignore list
  * [ ] find how many files only have a one-liner change
  * [ ] mark and detect refactorizations and ignore/group them
  * [ ] categorize changes
  * [ ] generate a nice summary of it all
