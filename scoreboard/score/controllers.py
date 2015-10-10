# Import flask dependencies
from flask import Blueprint, render_template

# Import the database object from the main app module
from flask.ext.login import current_user, login_required
from sqlalchemy.sql import functions, join, and_, or_
from checks import ServiceCheck, CheckResult
from checks.services import Service
from scoreboard.app import db
from scoring import FlagDiscovery, Flag, InjectSolve, Inject
from scoring.inject import team_inject_relation
from teams import Team

mod_scoring = Blueprint('scoring', __name__, url_prefix='/scoring')


def render_scoring_page(*args, **kwargs):
    kwargs['active_menu'] = 'scoring'
    kwargs['team'] = current_user.team
    return render_template(*args, **kwargs)

def render_inject_page(*args, **kwargs):
    kwargs['active_menu'] = 'injects'
    kwargs['team'] = current_user.team
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


@mod_scoring.route('/injects', methods=['GET'])
@login_required
def list_injects():
    team = current_user.team

    query = Inject.query
    if team.role == Team.WHITE:
        injects = query.all()
    else:
        injects = []
        for inject in team.available_injects:
            if inject.enabled:
                if inject.max_solves == -1 or team.inject_solves(inject) < inject.max_solves:
                    inject.can_solve = True
                else:
                    inject.can_solve = False

                injects.append(inject)


    return render_inject_page('scoring/injects.html', injects=injects)
