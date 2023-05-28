@echo off
pushd %~dp0
pushd "../"
python run.py %*
timeout /T 60 > nul