# ReeldIn

A website dedicated to personally tailoring your movie selection experience, ReeldIn is capable of generating personalized recommendations in under thirty seconds!
Designed to curb choice overload, this application is purely focused on finding you something to watch, improving upon the lackluster recommendations by movie-oriented social media sites and streaming services.

Created with Django, PSQL, and HTML/CSS/Javascript.

Formerly a Capstone Project for the University of Arizona's School of Information.

## External Usage

- <a href="https://github.com/michael-awe/django-template">django-template</a>
- <a href="https://github.com/FormBold/html-form-examples-templates">html-form-examples-templates</a>
- <a href="https://github.com/capwan/Animated-LoginForm">Animated-LoginForm</a>

Find licenses for externally used projects in 'documentation/external_licenses'. Find libraries in 'requirements.txt'.

## VSCode Extensions

- Black Formatter by Microsoft
- Pylance by Microsoft
- Prettier - Code formatter by Prettier
- Auto Rename Tag by Jun Han
- CSS Peek by Pranay Prakash

## Set-Up (Windows)
Note: This set-up has only been tested / confirmed working using Windows.

Make a 'ReeldIn' folder that'll hold our project and clone the repo:

    mkdir ReeldIn
    cd ReeldIn
    git clone https://github.com/jonathanhouge/ReeldIn.git .

Next, create and activate a virtual environment:

    python3 -m venv env
    source env/Scripts/activate

Now, you need to make a local database:

1.  Download PSQL
2.  In PGAdmin, right-click 'Databases' -> 'Create' -> 'Database', then name it and save.
3.  Now, you need your '.env' file! Contact the devs on acquiring that and the associated information.

Now install the dependencies from requirements.txt and run the set up script:

    pip install -r requirements.txt
    sh setup.sh

## Commands for Running & Developing Locally

To start tailwind:

    python manage.py tailwind start

To start your Django server:

    python manage.py runserver

Whenever you're formatting '.html' files, use this command:

    python -m djlint {html-file-path} --reformat --indent 2

## Debugging FAQ

**You've tried 'python manage.py runserver':**

"You have # unapplied migration(s). Your project may not work properly until you apply the migrations for app(s):
[list].
Run 'python manage.py migrate' to apply them."

Exactly as it sounds! 'python manage.py makemigrations' was already ran so you have the migration files, you've just got to run 'python manage.py migrate' to apply them to the associated tables.

**You've tried to run 'sh setup.sh':**

"CommandError: It looks like node.js and/or npm is not installed or cannot be found..."

Whoops! 'npm' can't be found. Go into 'settings.py' and find the variable 'NPM_BIN_PATH' and copy the absolute path to 'npm.cmd' on your computer.
