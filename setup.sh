#!/bin/bash
# check your shell scripts: https://www.shellcheck.net/

# valid '.env' file required for initializing database
if ! test -f ".env"; then
    echo "You don't have a '.env' file!"
    exit
fi

read -rp "Do you have a valid '.env' file? [y/n] " answer
case $answer in
    [yY] ) ;;
    [nN] ) echo "Go get one then!"
    exit;;
    
    * ) echo "ERROR: Invalid response. Exiting..."
    exit 1;;
    
esac

echo "Project setup begun."

echo "Downloading dependencies."
pip install -r requirements.txt

echo "Applying migrations."
python manage.py makemigrations && python manage.py migrate

echo "Initializing database."
python manage.py init_db "recommendations/fixtures/movies_fixture.json"

echo "Installing tailwind."
python manage.py tailwind install

echo "Project setup successful."