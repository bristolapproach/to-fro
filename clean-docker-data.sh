#!/bin/bash
docker rm -f tofro-django tofro-db
docker volume rm -f tofro_data_volume
