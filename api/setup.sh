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

# Create the admin user.
python3 manage.py shell < tools/create_admin.py

# Collect static files.
python3 manage.py collectstatic --noinput --clear

# Start a redis worker.
python manage.py rqworker default & > /dev/null 2>&1

# Start the redis scheduler.
python manage.py rqscheduler &

# Schedule our repeated tasks.
python manage.py schedule_tasks
