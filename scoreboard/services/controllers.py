# Import flask dependencies
from flask import Blueprint, render_template

# Import the database object from the main app module
from checks.service_checks import Service, ServiceCheck
from flask.ext.login import current_user, login_required

mod_services = Blueprint('services', __name__, url_prefix='/services')

@mod_services.route('/', methods=['GET'])
@login_required
def team_service_list():
    team = current_user.team

    return render_template('services/index.html', team=team)


@mod_services.route('/<service_id>', methods=['GET', 'POST'])
@login_required
def team_service_overview(service_id):
    service = Service.query.get(service_id)
    if service and current_user.team.id == service.team_id:
        return render_template('services/service.html', service_name='sad', service=service, team=current_user.team)
    return "no."

@mod_services.route('/<service_id>/<check_id>', methods=['GET', 'POST'])
@login_required
def team_service_check_overview(service_id, check_id):
    service = Service.query.get(service_id)
    check = ServiceCheck.query.get(check_id)
    if service and check and check in service.checks and current_user.team.id == service.team_id:
        return render_template('services/check.html', service_name='sad', service=service, check_name=':(', check=check, team=current_user.team)
    return "no."
