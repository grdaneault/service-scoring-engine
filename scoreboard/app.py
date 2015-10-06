import os
from flask import Flask, render_template_string
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy, _QueryProperty, BaseQuery
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from configuration.models import Models
from configuration.persistence import Base

import configuration.web_configuration
from teams.user import User


def create_app():
    """ Flask application factory """

    # Setup Flask app and app.config
    app = Flask(__name__)
    app.config.from_object(configuration.web_configuration.ConfigClass)

    # Initialize Flask extensions
    db = SQLAlchemy(app) # Initialize Flask-SQLAlchemy
    Base.query = _QueryProperty(db)
    Base.query_class = BaseQuery
    Models.create_tables(db.engine)

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User


    return app


# Start development web server
if __name__== '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)