#!/bin/zsh
git rm -r --cached .
git add *
git commit -m "$1"
git push