#!/bin/bash
git reset --hard origin/your-branch
git pull
pip install -r requirements.txt
echo "update complete"