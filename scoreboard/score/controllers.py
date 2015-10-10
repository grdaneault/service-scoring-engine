# Import flask dependencies
from flask import abort, Blueprint, redirect, url_for, render_template, flash

# Import the database object from the main app module
from flask.ext.login import current_user, login_required
from sqlalchemy.sql import functions, join, and_
from checks import ServiceCheck, CheckCredentials, CheckResult
from checks.services import Service
from scoreboard.app import db
from scoring import FlagDiscovery, Flag, InjectSolve
from teams import Team

mod_scoring = Blueprint('scoring', __name__, url_prefix='/scoring')


def render_scoring_page(*args, **kwargs):
    kwargs['active_menu'] = 'credentials'
    return render_template(*args, **kwargs)


@mod_scoring.route('/', methods=['GET'])
@login_required
def team_score_list():
    teams = Team.query.filter_by(role=Team.BLUE)
    scoring_teams = []
    for team in teams:
        temp = db.session.query(
                functions.sum(CheckResult.success * ServiceCheck.value),
                functions.sum(ServiceCheck.value)) \
            .select_from(
                join(CheckResult,
                     join(ServiceCheck, Service, ServiceCheck.service_id == Service.id),
                     CheckResult.check_id == ServiceCheck.id))

        services = temp.filter(Service.team_id == team.id).first()

        earned = 0
        maximum = 0
        if services:
            earned = services[0]
            maximum = services[1]

        # select sum(c*v) from (SELECT count(*) as c, value as v FROM `flag_discovery` join flag on flag.id = flag_discovery.flag_id where flag.team_id = 2 group by flag.id) as ttt;
        flag_subquery = db.session.\
            query(functions.count(FlagDiscovery.id).label('solve_count'), Flag.value).\
            select_from(join(Flag, FlagDiscovery, Flag.id == FlagDiscovery.flag_id)).\
            filter(Flag.team_id == team.id).\
            group_by(Flag.id).\
            subquery('flag_subquery')
        flags = db.session \
            .query(functions.sum(flag_subquery.c.solve_count * flag_subquery.c.value)).\
            first()

        flags = flags[0] if flags[0] else 0

        injects = db.session \
            .query(functions.sum(InjectSolve.value_approved)) \
            .filter(and_(InjectSolve.team_id == team.id, InjectSolve.approved == True)) \
            .first()

        injects = injects[0] if injects[0] else 0

        team.scores = {
            'services_earned': earned,
            'services_maximum': maximum,
            'injects_earned': injects,
            'flags_lost': flags
        }

        scoring_teams.append(team)

    return render_scoring_page('scoring/index.html', teams=scoring_teams)
