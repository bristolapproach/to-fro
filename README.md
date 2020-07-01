# To-Fro

We're working on a system that can be used by different communities to help self organise, keep track of need and effectively deploy help.

## Development environment

To get started, download docker, clone this repository, then start the database and the Django server in the foreground using this command:

    docker-compose up --build

Configuration is handled via the `.env` file. Environment variables will override what's defined in the `.env` file.

If `DEBUG=True`, then Django's development server will be used. This includes hot-reload from code changes, and additional log information. If `DEBUG=False`, a production `gunicorn` server will be used.

During development, you can enable Django's hot-reload functionality by mounting the source code as a volume into the container. This maps your local directory with a directory in the docker container. To do this, change the command above to:

    docker-compose -f docker-compose.yml -f development.yml up --build

The benefit of mounting your local filesystem into the docker container is both avoiding installing dependencies locally, and to avoid reloading the container every time you write some code.

To execute a python command on the docker container, use a command like this:

    docker exec -it tofro-django python manage.py startapp test

You can see the names of the running containers with `docker ps`.

## Frontend assets

The styles and scripts of the app are build with [ParcelJS](https://parceljs.org/) from the sources in `api/assets/src`. The files are compiled to the `api/assets/static` folder to match [Django's conventions for static folders](https://docs.djangoproject.com/en/3.0/howto/static-files/#configuring-static-files).

The build happens at container startup so you shouldn't have anything to do if you're just editing backend code. For development, you can run `npm run dev` inside the Django container to monitor your files and rebuild on change:

    docker exec -it tofro-django npm run dev

Equally, you can run `npm install` to install new modules from inside the Django container too:

    docker exec -it tofro-django npm install

## Application messages

The application relies on 3rd party packages whose messages needed to be overriden. This is done by taking advantage of [Django's localization system](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#localization-how-to-create-language-files), with a special language file in the `api/messages_overrides` folder, as described by [this StackOverflow answer](https://stackoverflow.com/a/41945558).

To override a piece of text coming from a 3rd party package:

1. Check that the piece of text is computed via Django's translation utilities. This can be a call to one of the `gettext()` methods (often aliased as `_()`) or using the `{% translate %}` tag.
2. Grab the ID of the message. This will be the string passed to the method or tag.
3. Add an entry to the `messages_overrides/en/LC_MESSAGES/django.po` file, as such:

    msgid "THE_ID_FOUND_IN_THE_3RD_PARTY_PACKAGE"
    msgstr "THE_MESSAGE_YOU_WANT_TO_SHOW"

    Pay attention to the case, as the `msgid` is case sensitive
4. Compile the messages with:

    docker exec -it tofro-django python3 manage.py compilemessages

## Testing

To check that everything works OK, there is a [manual testing plan in the TESTING.md](./TESTING.md) file.
