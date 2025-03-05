#!/bin/bash
# check your shell scripts: https://www.shellcheck.net/

echo "Welcome to the ReeldIn set-up!"
echo "We'll do some validation and then get everything started."
echo "CTRL + C if you need to stop this script at any point."
read -rp "Press any key to continue. " answer
case $answer in
    * ) ;;
    
esac

echo

if test -f "setup-successful.txt"; then
    read -rp "It looks like you've successfully ran this script before - do you still wish to continue? [y/n] " answer
    case $answer in
        [yY] ) ;;
        [nN] ) exit;;
        
        * ) echo "ERROR: Invalid response. Exiting..."
        exit 1;;
        
    esac
fi

# valid '.env' file required for initializing database
if ! test -f ".env"; then
    echo "You need a '.env' file to run ReeldIn, '.env_sample' should be used as a template."
    echo "Run this script again when you have one."
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

echo "Validation complete. Project setup begun."

echo

echo "Installing requirements."
pip install -r requirements.txt

python manage.py tailwind install

if ! test -f ".stylelintrc.json"; then
    echo "Installing stylelint."
    npm init stylelint
fi

echo
read -rp "Requirements installed. Press any key to initialize the database. " answer
case $answer in
    * ) ;;
    
esac

echo "Applying migrations."
python manage.py makemigrations && python manage.py migrate

echo

echo "Initializing database."
python manage.py init_db "recommendations/fixtures/movies_fixture.json"

echo

echo "Database successfully initialized."
read -rp "Project setup complete. Press any key to exit. " answer
case $answer in
    * ) ;;
    
esac

echo "ReeldIn 'setup.sh' was ran successfully!" > successful-setup.txt
date >> successful-setup.txt