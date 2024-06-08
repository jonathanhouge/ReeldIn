echo "Project setup begun."
echo "Note: Make sure you have a valid '.env' file before running."

echo "Downloading dependencies."
pip install -r requirements.txt

echo "Applying migrations."
python manage.py makemigrations && python manage.py migrate

echo "Initializing database."
python manage.py loaddata "recommendations/fixtures/movies_fixture.json"

echo "Installing tailwind."
python manage.py tailwind install

echo "Project setup successful."
