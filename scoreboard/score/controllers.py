# Import flask dependencies
import datetime
from flask import abort, Blueprint, render_template

# Import the database object from the main app module
from flask.ext.login import current_user, login_required
from sqlalchemy.sql import functions, join, and_, or_
from checks import ServiceCheck, CheckResult
from checks.services import Service
from scoreboard.app import db
from scoreboard.score.inject_rules import score_injects, can_submit_inject, has_pending_solve, solve_count
from scoring import FlagDiscovery, Flag, InjectSolve, Inject
from teams import Team

mod_scoring = Blueprint('scoring', __name__, url_prefix='/scoring')


def render_scoring_page(*args, **kwargs):
    kwargs['active_menu'] = 'scoring'
    kwargs['team'] = current_user.team
    return render_template(*args, **kwargs)

def render_inject_page(*args, **kwargs):
    kwargs['active_menu'] = 'injects'
    kwargs['team'] = current_user.team
    kwargs['can_submit_inject'] = can_submit_inject
    kwargs['has_pending_solve'] = has_pending_solve
    kwargs['solve_count'] = solve_count

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

        injects = score_injects(team)

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
def list_available_injects():
    team = current_user.team

    query = Inject.query
    if team.role == Team.WHITE:
        injects = query.all()
        return render_inject_page('scoring/injects-admin.html', injects=injects)
    else:
        injects = [inject for inject in team.available_injects if inject.is_visible()]
        return render_inject_page('scoring/injects.html', injects=injects)


@mod_scoring.route('/injects/complete/<inject_id>', methods=['GET'])
@login_required
def solve_inject(inject_id):
    team = current_user.team
    inject = Inject.query.get(inject_id)
    if not inject:
        abort(404)
        return "no."

    if not inject.enabled:
        abort(401)
        return "no."

    if not team.can_submit_inject(inject):
        abort(401)
        return "can't resolve."

    team.solved_injects.append(InjectSolve(team_id=team.id, inject=inject, date_requested=datetime.datetime.now()))
    db.session.commit()

    return render_inject_page('scoring/injects.html', injects=[])

@mod_scoring.route('/injects/manage/solve/<solve_id>/<approve>', methods=['GET'])
@login_required
def manage_solve(solve_id, approve):
    return "todo"

@mod_scoring.route('/injects/manage/inject/<inject_id>/open', methods=['GET'])
@login_required
def open_inject(inject_id):
    return 'todo'

@mod_scoring.route('/injects/manage/inject/<inject_id>/close', methods=['GET'])
@login_required
def close_inject(inject_id):
    return 'todo'
