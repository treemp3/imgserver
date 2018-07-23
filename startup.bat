@echo off
title ImgService
rem taskkill /f /t /im python.exe
cd /d %~dp0
python __main__.py
