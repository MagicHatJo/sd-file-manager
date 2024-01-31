#!/bin/bash

##### variables #####
python_cmd="python3.10"
required_version="3.10.0"
venv_dir=".venv"
use_venv=1
config_file="config.json"
main="sd-file-manager"

##### python #####
if command -v "$python_cmd" &>/dev/null
then
	python_version=$("$python_cmd" --version 2>&1 | awk '{print $2}')
	if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]
	then
		printf "Error: Python $required_version or later is required. Current version is $python_version.\n"
		exit 1
	else
		printf "$python_cmd $required_version or later is installed.\n"
	fi
else
    printf "Error: $python_cmd is not installed. Please install $python_cmd $python_version or later before running this script.\n"
    exit 1
fi

##### venv #####
if [[ $use_venv -eq 1 ]] && [[ -z "${VIRTUAL_ENV}" ]]
then
	if ! "${python_cmd}" -c "import venv" &>/dev/null
	then
		printf "\e[1m\e[31mERROR: python3-venv is not installed, aborting...\e[0m\n"
		exit 1
	fi

	if [[ ! -d "${venv_dir}" ]]
	then
		"${python_cmd}" -m venv "${venv_dir}"
	fi

	if [[ -f "${venv_dir}"/bin/activate ]]
	then
		printf "Activating venv.\n"
		source "${venv_dir}"/bin/activate
	else
		printf "\e[1m\e[31mERROR: Cannot activate python venv, aborting...\e[0m\n"
		exit 1
	fi
else
	printf "Python venv already activated.\n"
fi

##### requirements #####
pip install -r requirements.txt

##### config #####
if [ ! -f "$config_file" ]
then
	printf "Creating config.json from template.\n"
	cp "config-template.json" "config.json"
else
	printf "${config_file} set as config.\n"
fi

##### launch #####
printf "Launching ${main}.\n"
"${python_cmd}" "${main}.py"