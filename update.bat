@echo off
git pull -s recursive -X theirs
pip install requirements.txt
echo "update complete"
pause