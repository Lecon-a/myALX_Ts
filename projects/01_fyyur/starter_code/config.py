import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
username = "postgres"
password = "usepass"
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@127.0.0.1/fyyurdb'.format(username, password)
SQLALCHEMY_TRACK_MODIFICATIONS = False
