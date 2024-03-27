@echo off
set mypath=%~dp0
set conf_folder=%mypath%\src\configuration
set dist_folder=%mypath%\src\dist
pyinstaller confmanager.spec
robocopy /s "%conf_folder%" "%dist_folder%\configuration"
pause