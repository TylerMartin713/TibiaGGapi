#!/bin/bash

rm db.sqlite3
rm -rf ./TibiaGGapi/migrations
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py migrate
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py makemigrations TibiaGGapi
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py migrate TibiaGGapi
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py loaddata users
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py loaddata tokens
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py loaddata locations
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py loaddata comments
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py loaddata vocations
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py loaddata character
/home/tylermartin713/.pyenv/versions/3.12.3/bin/python manage.py loaddata huntingplace

