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
python3 manage.py shell < tools/create_admin.py


# Collect static files.
python3 manage.py collectstatic --noinput --clear

# Determine whether to serve over HTTP or HTTPS.
if [[ ! -z ${DJANGO_HTTPS} && ! -z ${HOSTNAME} ]]; then
    
    # Generate certificates.
    openssl req -new -nodes -x509 \
        -subj "/C=GB/ST=Avon/L=Bristol/O=IT/CN=${HOSTNAME}" \
        -days 3650 -keyout server.key \
        -out server.crt \
        -extensions v3_ca
    
    # Serve over HTTPS.
    gunicorn --certfile=server.crt --keyfile=server.key \
             --capture-output --enable-stdio-inheritance \
             --worker-tmp-dir /dev/shm --workers=2 \
             --threads=4 --worker-class=gthread \
             --bind :${DJANGO_PORT} tofro.wsgi
else
    # Serve over HTTP.
    gunicorn --capture-output --enable-stdio-inheritance \
             --worker-tmp-dir /dev/shm --workers=2 \
             --threads=4 --worker-class=gthread \
             --bind :${DJANGO_PORT} tofro.wsgi
fi
