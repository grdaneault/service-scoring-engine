# Import flask dependencies
import datetime
from flask import abort, Blueprint, flash, render_template, redirect, url_for

# Import the database object from the main app module
from flask.ext.login import current_user, login_required
from sqlalchemy.sql import functions, join, and_, or_
from checks import ServiceCheck, CheckResult
from checks.services import Service
from scoreboard.app import db, flash_errors
from scoreboard.score.forms import InjectApprovalForm
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
    teams = Team.query.filter(Team.role.in_([Team.BLUE, Team.RED]))
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
        if services[0]:
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

    if not inject.can_submit():
        abort(401)
        return "no."

    if not can_submit_inject(team, inject):
        abort(401)
        return "can't resolve."

    team.solved_injects.append(InjectSolve(team_id=team.id, inject=inject, date_requested=datetime.datetime.now()))
    db.session.commit()

    return render_inject_page('scoring/injects.html', injects=[])

@mod_scoring.route('/injects/manage/solve/<solve_id>/reject', methods=['GET'])
@login_required
def reject_solve(solve_id):
    if not current_user.team.role == Team.WHITE:
        abort(401)
        return "no."

    solve = InjectSolve.query.get(solve_id)
    if not solve:
        flash('No solve with that ID exists', category='danger')
        return redirect(url_for('scoring.list_available_injects'))

    solve.reject(current_user)
    db.session.commit()
    flash('Solve request rejected', category='success')
    return redirect(url_for('scoring.list_available_injects'))

@mod_scoring.route('/injects/manage/solve/<solve_id>/approve', methods=['GET', 'POST'])
@login_required
def approve_solve(solve_id):
    if not current_user.team.role == Team.WHITE:
        abort(401)
        return "no."

    solve = InjectSolve.query.get(solve_id)
    if not solve:
        flash('No solve with that ID exists', category='danger')
        return redirect(url_for('scoring.list_available_injects'))

    form = InjectApprovalForm()
    if form.validate_on_submit():
        solve.approve(current_user, int(form.value.data))
        db.session.commit()
        flash('Awarded %s points to %s for solving %s' % (form.value.data, solve.team.name, solve.inject.title))
        return redirect(url_for('scoring.list_available_injects'))
    else:
        flash_errors(form)

    return render_inject_page('scoring/injects-approve.html', form=form, solve=solve)


@mod_scoring.route('/injects/manage/inject/<inject_id>/open', methods=['GET'])
@login_required
def open_inject(inject_id):
    if not current_user.team.role == Team.WHITE:
        abort(401)
        return "no."

    inject = Inject.query.get(inject_id)
    if not inject:
        abort(404)
        return 'inject not found'

    if inject.is_visible():
        flash('Inject %s (%s) is already open.' % (inject.title, inject.id), category='danger')
    else:
        inject.open()
        db.session.commit()
        flash('Inject %s (%s) Opened!.' % (inject.title, inject.id), category='success')

    return redirect(url_for('scoring.list_available_injects'))

@mod_scoring.route('/injects/manage/inject/<inject_id>/close', methods=['GET'])
@login_required
def close_inject(inject_id):
    if not current_user.team.role == Team.WHITE:
        abort(401)
        return "no."

    inject = Inject.query.get(inject_id)
    if not inject:
        abort(404)
        return 'inject not found'

    if not inject.is_visible():
        flash('Inject %s (%s) is already closed.' % (inject.title, inject.id), category='danger')
    else:
        inject.close()
        db.session.commit()
        flash('Inject %s (%s) Closed!' % (inject.title, inject.id), category='success')

    return redirect(url_for('scoring.list_available_injects'))
