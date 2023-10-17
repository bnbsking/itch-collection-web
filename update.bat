@echo off
git reset --hard origin/main
git pull
pip install -r requirements.txt
echo "update complete"
pause