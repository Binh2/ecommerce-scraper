@echo off
pushd %~dp0
pushd "../"
python run.py -w shopee %*
timeout /T 60 > nul