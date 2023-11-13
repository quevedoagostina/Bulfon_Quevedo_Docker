#!/bin/bash

# Sleep for 10 seconds before running migrations
echo 'Sleeping for 10 seconds...'
sleep 10

echo 'Running database migrations'
export PYTHONPATH=/usr/local/lib/python3.9/site-packages:/path/to/marshmallow
export FLASK_APP=app/app.py
flask db init
flask db migrate
flask db upgrade

echo 'Starting Gunicorn server'
gunicorn -b 0.0.0.0:5005 app.app:app