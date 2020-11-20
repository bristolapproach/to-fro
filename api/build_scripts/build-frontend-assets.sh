#!/bin/bash


if [[ ! ($RUN_ENV == "local-dev" || $RUN_ENV == "dev" || $RUN_ENV == "prod") ]]; then
  echo "error: RUN_ENV must be one of: 'local-dev', 'dev', 'prod'"; exit 1
fi

TOFRO_API_BASE_DIR=/code

if [[ $RUN_ENV == "local-dev" || $RUN_ENV == "dev" ]]; then
  NODE_ENV=development
  parcel build "$TOFRO_API_BASE_DIR/static-src/*" -d "$TOFRO_API_BASE_DIR/parcel-built" --public-url '.' --no-minify
else
  NODE_ENV=production
  parcel build "$TOFRO_API_BASE_DIR/static-src/*" -d "$TOFRO_API_BASE_DIR/parcel-built" --public-url '.'
fi

python /code/manage.py collectstatic --noinput --clear