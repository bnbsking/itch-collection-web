#!/bin/bash
git reset --hard HEAD~1
git pull -s recursive -X theirs
pip install -r requirements.txt
echo "update complete"