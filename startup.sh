#!/bin/bash
# check your shell scripts: https://www.shellcheck.net/

if ! test -f "successful-setup.txt"; then
    echo "It looks you haven't ran setup.sh before - you should run that first!"
    read -rp "Press enter to exit." answer
    case $answer in
        * ) ;;
        
    esac
    
    echo
    
    exit 1
fi

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This file needs to be ran using the source command."
    echo "The source command is only available on Linux terminals."
    read -rp "Press enter to exit. " answer
    case $answer in
        * ) ;;
        
    esac
    
    echo
    
    exit 1
fi

time=$(date '+%H')

if [ "$time" -lt 6 ]; then
    greeting="zzzzzzzZZZZZZZzZZzzZzZ"
    elif [ "$time" -lt 12 ]; then
    greeting="Good morning!"
    elif [ "$time" -lt 17 ]; then
    greeting="Good afternoon!"
    elif [ "$time" -lt 22 ]; then
    greeting="Good evening!"
    elif [ "$time" -lt 24 ]; then
    greeting="I'm a little tired, are you tired?"
fi

echo "$greeting"
echo "Let's get you up and running!"
echo "CTRL + C if you need to stop this script at any point."
echo

echo "Activating virtual environment..."
echo

source env/Scripts/activate

echo "Ensuring upgrader packages are installed..."
echo

pip install pur
npm i -g npm-check-updates

echo
echo "Checking for updates and installing any found..."
echo

pur --minor django
pip install -r requirements.txt
ncu -u
npm install

echo
echo "Starting server..."
echo

python manage.py runserver