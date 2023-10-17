#!/bin/bash
cd ..
git clone https://github.com/bnbsking/itch-collection-web.git tmp
rm -r itch-collection-web
mv tmp itch-collection-web
cd itch-collection-web
pip install requirements.txt