@echo off
set "script_path=%~dp0"
set "script_path=%script_path%fbx.py %CD%"
python %script_path% %*