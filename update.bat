@echo off
cd ..
git clone https://github.com/bnbsking/itch-collection-web.git tmp
rmdir /s /q itch-collection-web
rename tmp itch-collection-web