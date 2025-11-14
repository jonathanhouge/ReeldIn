#!/bin/bash
# check your shell scripts: https://www.shellcheck.net/

source env/Scripts/activate

echo "Checking for any updates..."
echo

pur --minor django
npm i -g npm-check-updates
ncu -u
npm install

echo
echo "Starting server..."
echo

python manage.py runserver

