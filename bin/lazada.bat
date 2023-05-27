@echo off
pushd %~dp0
pushd "../"
python main.py -w lazada %*
timeout /T 60 > nul