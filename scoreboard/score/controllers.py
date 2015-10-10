# Import flask dependencies
from flask import abort, Blueprint, redirect, url_for, render_template, flash

# Import the database object from the main app module
from flask.ext.login import current_user, login_required
from sqlalchemy.sql import functions, join
from checks import ServiceCheck, CheckCredentials, CheckResult
from checks.services import Service
from scoreboard.app import db
from scoreboard.credentials.forms import PasswordChangeForm
from teams import Team

mod_scoring = Blueprint('scoring', __name__, url_prefix='/scoring')

def render_scoring_page(*args, **kwargs):
    kwargs['active_menu'] = 'credentials'
    return render_template(*args, **kwargs)

@mod_scoring.route('/', methods=['GET'])
@login_required
def team_score_list():
    teams = Team.query.filter_by(role=Team.BLUE)
    for team in teams:
        earned, maximum = db.session\
            .query(functions.sum(CheckResult.success * ServiceCheck.value),
                   functions.sum(ServiceCheck.value))\
            .select_from(
                join(CheckResult, join(ServiceCheck, Service, ServiceCheck.service_id == Service.id), CheckResult.check_id == ServiceCheck.id))\
            .filter(Service.team_id == Team.id)\
            .all()

        team.scores = {
            'earned': earned,
            'maximum': maximum
        }

    return render_scoring_page('credentials/index.html', teams=teams)


