# modified from original implementation

echo "Project setup begun."

# Make database migrations
python manage.py makemigrations && python manage.py migrate
echo "Migration successful."

# Load movies into database
python manage.py loaddata "recommendations/fixtures/movies_fixture.json"
echo "Database initialized."

# Install tailwind dependencies
python manage.py tailwind install
echo "Tailwind install successful."

echo "Project setup complete."
