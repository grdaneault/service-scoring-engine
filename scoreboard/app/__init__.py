from flask import Flask
from flask.ext.user import SQLAlchemyAdapter, UserManager
from flask_sqlalchemy import SQLAlchemy, _QueryProperty, BaseQuery

from configuration.models import create_tables
from configuration.persistence import Base
import configuration.web_configuration
from teams.user import User

app = Flask(__name__)
app.config.from_object(configuration.web_configuration.ConfigClass)

# Initialize Flask extensions
db = SQLAlchemy(app) # Initialize Flask-SQLAlchemy

# Add needed query support to base class TODO: investigate difference from db.Model
Base.query = _QueryProperty(db)
Base.query_class = BaseQuery
create_tables(db.engine)

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

def register_modules():
    from scoreboard.status.controllers import mod_status as status_module
    from scoreboard.services.controllers import mod_services as services_module
    from scoreboard.credentials.controllers import mod_credentials as credentials_module
    from scoreboard.score.controllers import mod_scoring as scoring_module

    app.register_blueprint(status_module)
    app.register_blueprint(services_module)
    app.register_blueprint(credentials_module)
    app.register_blueprint(scoring_module)

# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
