
# Sleep for 20 seconds before running migrations
echo 'Sleeping for 20 seconds...'
sleep 20

# Use wait-for-it.sh to wait for MySQL to be available
./wait-for-it.sh bulfon_quevedo_mysql:3306 -t 120

# Running database migrations
export PYTHONPATH=/usr/local/lib/python3.9/site-packages:/path/to/marshmallow
export FLASK_APP=app.app:app
flask db init
flask db migrate
flask db upgrade

# Starting Gunicorn server
gunicorn -b 0.0.0.0:5005 app.app:app
