# To-Fro

We're working on a system that can be used by different communities to help self organise, keep track of need and effectively deploy help.

## Development environment

To get started, download docker and clone this repository.

Run `docker-compose up` to start the database and Django server in the foreground. Configuration is handled via the `.env` file. Environment variables will override what's defined in the `.env` file.

If `DEBUG=True`, then Django's development server will be used. This includes hot-reload from code changes, and additional log information. If `DEBUG=False`, a production `gunicorn` server will be used.

A volume mount defined in `docker-compose.yml` maps your local directory with that in the docker container.

    server:
        ...
        volumes:
        - "./:/code"

This allows you to execute commands on the running Python container (e.g. `python manage.py startapp test`) and have the results in your local filesystem. The benefit of this is avoiding installing dependencies locally.

To execute a python command on the docker container, use a command like this:

    docker exec -it tofro-django python manage.py startapp test

You can see the names of the running containers with `docker ps`.
