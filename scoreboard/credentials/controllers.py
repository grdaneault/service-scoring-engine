# Import flask dependencies
from flask import Blueprint, render_template

# Import the database object from the main app module
from flask.ext.login import current_user, login_required
from checks import ServiceCheck, CheckCredentials
from checks.services import Service

mod_credentials = Blueprint('credentials', __name__, url_prefix='/credentials')

def render_credentials_page(*args, **kwargs):
    kwargs['active_menu'] = 'services'
    return render_template(*args, **kwargs)

@mod_credentials.route('/', methods=['GET'])
@login_required
def team_credentials_list():
    team = current_user.team
    credentials = team.credentials

    return render_credentials_page('credentials/index.html',
                                   team=team,
                                   credentials=credentials)


