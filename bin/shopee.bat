@echo off
cd %~dp0
cd ../
python main.py -w shopee %*
timeout /T 60 > nul