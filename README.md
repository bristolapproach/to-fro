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

## Frontend assets

The styles and scripts of the app are build with [ParcelJS](https://parceljs.org/) from the sources in `assets/src`. The files are compiled to the `assets/static` folder to match [Django's conventions for static folders](https://docs.djangoproject.com/en/3.0/howto/static-files/#configuring-static-files).

The build happens at container startup so you shouldn't have anything to do if you're just editing backend code. If you need to edit the styles or scripts for the app, you'll need to have [NodeJS installed (12.X)](https://nodejs.org/en/).
You can then run the following to rebuild the files when you change them in the `assets/src` folder:

    npm run dev

If the command complains about missing modules, check that you have a `node_modules` folder at the root of the project. If it's missing, run the following command to install the NodeJS modules:

    npm install