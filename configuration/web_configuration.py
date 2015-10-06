# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
import os


class ConfigClass(object):
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://greg:greg@192.168.243.100/scoring_engine')
    CSRF_ENABLED = True

    USER_ENABLE_EMAIL = False

    # Flask-User settings
    USER_APP_NAME = "Scoreboard"
