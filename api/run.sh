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
