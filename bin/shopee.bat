@echo off
pushd %~dp0
pushd "../"
python main.py -w shopee %*
timeout /T 60 > nul