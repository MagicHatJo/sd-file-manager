@echo off
setlocal enabledelayedexpansion

REM Variables
set python_cmd=py
set required_version=3.10.0
set venv_dir=venv
set use_venv=1
set config_file=config.json
set main=sd-file-manager

REM Python
where %python_cmd% >nul 2>nul
if %errorlevel% == 0 (
	for /f "tokens=2 delims= " %%v in ('%python_cmd% --version 2^>^&1') do set "python_version=%%v"
	if "!required_version!" geq "!python_version!" (
		echo Error: Python !required_version! or later is required. Current version is !python_version!.
		exit /b 1
	) else (
		echo %python_cmd% !required_version! or later is installed.
	)
) else (
	echo Error: %python_cmd% is not installed. Please install %python_cmd% !required_version! or later before running this script.
	exit /b 1
)

REM Venv
if %use_venv% equ 1 (
    if not defined VIRTUAL_ENV (
        if not exist "%venv_dir%" (
			!python_cmd! -m venv %venv_dir%
		)
        if exist "%venv_dir%\Scripts\activate" (
            echo Activating venv.
            call "%venv_dir%\Scripts\activate"
        ) else (
            echo ERROR: Cannot activate python venv, aborting...
            exit /b 1
        )
    ) else (
        echo Python venv already activated.
    )
)

REM Requirements
pip install -r requirements.txt

REM Config
if not exist "%config_file%" (
    echo Creating config.json from template.
    copy "config-template.json" %config_file%
) else (
    echo %config_file% set as config.
)

REM Launch
echo Launching %main%.
%python_cmd% %main%.py