@echo off
pushd %~dp0
pushd "../"
python main.py %*
timeout /T 60 > nul