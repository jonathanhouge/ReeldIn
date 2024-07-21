#!/bin/bash
# check your shell scripts: https://www.shellcheck.net/

if ! test -d "env"; then
    echo "You don't have a virtual environment!? Let's fix that."
    python3 -m venv env
fi

source env/Scripts/activate

# TODO check out 'pip-upgrade' to make sure 'requirements.txt' is always up-to-date
# https://stackoverflow.com/questions/24764549/upgrade-python-packages-from-requirements-txt-using-pip-command
#pip-upgrade
