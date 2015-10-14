from flask import Flask, flash
from flask.ext.user import SQLAlchemyAdapter, UserManager
from flask_sqlalchemy import SQLAlchemy, _QueryProperty, BaseQuery
from jinja2 import evalcontextfilter, Markup, escape
import re

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
    from scoreboard.users.controllers import mod_users as users_module

    app.register_blueprint(status_module)
    app.register_blueprint(services_module)
    app.register_blueprint(credentials_module)
    app.register_blueprint(scoring_module)
    app.register_blueprint(users_module)

    _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

    @app.template_filter()
    @evalcontextfilter
    def nl2br(eval_ctx, value):
        result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
                              for p in _paragraph_re.split(escape(value)))
        if eval_ctx.autoescape:
            result = Markup(result)
        return result

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % error, category='danger')

# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
