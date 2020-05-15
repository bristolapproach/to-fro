# Ensure the container stops if an error occurs.
set -e

# Wait for the database to come online.
while ! nc -z ${DATABASE_HOST} ${DATABASE_PORT}; do 
    echo "Waiting for DB at '${DATABASE_HOST}:${DATABASE_PORT}'"
    sleep 1
done

# Build the front-end assets
npm install
npm run build

# Set up the data migrations.
python3 manage.py makemigrations
python3 manage.py migrate

# Sets the site domain for the Sites app
python3 manage.py set_site_domain

# Create the admin user.
python3 manage.py create_admin

# Create the navigation menu
python3 manage.py create_main_navigation_menu

# Collect static files.
python3 manage.py collectstatic --noinput --clear

# Run the Django server.
python manage.py runserver 0:${DJANGO_PORT}
