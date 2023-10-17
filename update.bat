@echo off
git reset --hard origin/your-branch
git pull
pip install -r requirements.txt
echo "update complete"
pause