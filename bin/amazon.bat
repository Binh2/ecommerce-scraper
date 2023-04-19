@echo off
cd %~dp0
cd ../
python main.py %*
timeout /T 60 > nul