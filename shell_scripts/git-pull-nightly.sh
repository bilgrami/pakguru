#!/bin/bash
git branch -a
git checkout origin/nightly
git checkout nightly
# gitk --all
# If you have many remote branches that you want to fetch at once, do:
git pull --all
