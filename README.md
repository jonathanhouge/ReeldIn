# ReeldIn

A website dedicated to personally tailoring your movie selection experience, generating personalized recommendations in under thirty seconds!
Allows one to curb choice overload and is purely focused on finding you something to watch, improving upon the lackluster recommendations by movie-oriented social media sites and streaming services.

Created with Django, PSQL, and HTML/CSS/Javascript.

Formerly a Capstone Project for the University of Arizona's School of Information.

## External Usage

Find licenses for externally used projects in 'documentation/external_licenses'.

Uses <a href="https://github.com/michael-awe/django-template">django-template</a>, <a href="https://github.com/FormBold/html-form-examples-templates">html-form-examples-templates</a>, and <a href="https://github.com/capwan/Animated-LoginForm">Animated-LoginForm</a>.

Watch the videos found in 'documentation/video_urls.txt' and read what's below. If there's
conflicting information, follow what's written here instead. (need to be updated)

## VSCode Extensions

- Black Formatter by Microsoft
- Pylance by Microsoft
- Prettier - Code formatter by Prettier

## Set-Up (Windows)

Make a 'ReeldIn' folder that'll hold our project and clone the repo:

    mkdir Implementation
    cd Implementation
    git clone https://github.com/jonathanhouge/ReeldIn.git .

Next, create and activate a virtual environment:

    python3 -m venv env
    source env/Scripts/activate

Now install the dependencies from requirements.txt and run the set up script:

    pip install -r requirements.txt
    sh setup.sh

Now, you need to make a local database! Here's how we do it. (I used this <a href="https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8">guide</a>, step six and on)
1. Download PSQL
2. In PGAdmin, right-click 'Databases' -> 'Create' -> 'Database', then name it and save.
3. Now, you need your '.env' file! Contact the devs on acquiring that and the associated information.
4. Now, in the repo, apply migrations and utilize the fixture.

        python manage.py migrate
        python manage.py loaddata "recommendations/fixtures/movies_fixtures.json"

## Running Locally

In order to use Tailwind, you'll have to create two terminal tabs, one to start tailwind and the other to start your Django server

In the first terminal type:

    python manage.py tailwind start

You can then start your Django server in a separate tab like this:

    python manage.py runserver

You're now all set and ready to start developing!

## Debugging Set-Up Process

**You've tried 'python manage.py runserver' and seen this error:**

"You have # unapplied migration(s). Your project may not work properly until you apply the migrations for app(s):
[list].
Run 'python manage.py migrate' to apply them."

Exactly as it sounds! 'python manage.py makemigrations' was already ran so you have the migration files, you've just
got to run 'python manage.py migrate' to make them run.

**You've tried to run 'sh setup.sh' and seen this error:**

"CommandError: It looks like node.js and/or npm is not installed or cannot be found..."

Whoops! 'npm' can't be found. Go into 'settings.py' and find the variable 'NPM_BIN_PATH' and copy the absolute
path to 'npm.cmd' on your computer.
