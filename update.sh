#!/bin/bash
git reset --hard HEAD^
git pull -s recursive -X theirs
pip install requirements.txt
echo "update complete"