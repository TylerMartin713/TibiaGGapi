#!/bin/bash

rm db.sqlite3
rm -rf ./TibiaGGapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations TibiaGGapi
python3 manage.py migrate TibiaGGapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

