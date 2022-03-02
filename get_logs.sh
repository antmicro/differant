#!/bin/bash

set -e

if [ $# -lt 2 ]; then
    echo "Please provide the repo to parse as arguments."
    exit 1
fi

CURDIR=`pwd`

COMMIT_OR_TAG=$2
REPO_NAME=`basename $1`
cd $1
git --no-pager log $COMMIT_OR_TAG..HEAD --pretty=format:"%C(yellow)%h%Creset | %C(cyan)%C(bold)%ad%Creset | %s" --date=format:'%Y-%m-%d,%H:%M:%S' > $CURDIR/$REPO_NAME.log
cd - > /dev/null
