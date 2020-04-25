# Ensure the container stops if an error occurs.
set -e

# Wait for the database to come online.
while ! nc -z ${DATABASE_HOST} ${DATABASE_PORT}; do 
    echo "Waiting for DB at '${DATABASE_HOST}:${DATABASE_PORT}'"
    sleep 1
done

# Set up the data migrations.
python3 manage.py makemigrations
python3 manage.py migrate

# Create the admin user.
python3 manage.py shell < tools/create_admin.py

# Collect static files.
python3 manage.py collectstatic --noinput --clear

# Run the Django server.
python manage.py runserver 0:${DJANGO_PORT}
