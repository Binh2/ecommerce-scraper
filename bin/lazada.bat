@echo off
pushd %~dp0
pushd "../"
python run.py -w lazada %*
timeout /T 60 > nul