@echo off
title FaroFinder
cd /d "%~dp0"
".venv\Scripts\python.exe" -m buscador %*
if errorlevel 1 pause
