# Import flask dependencies
from flask import Blueprint, render_template

# Import the database object from the main app module
from checks.service_checks import Service, ServiceCheck, CheckCredentials
from flask.ext.login import current_user, login_required

mod_services = Blueprint('services', __name__, url_prefix='/services')

def render_services_page(*args, **kwargs):
    kwargs['active_menu'] = 'services'
    return render_template(*args, **kwargs)

@mod_services.route('/', methods=['GET'])
@login_required
def team_service_list():
    team = current_user.team

    return render_services_page('services/index.html',
                           team=team)


@mod_services.route('/<service_id>', methods=['GET', 'POST'])
@login_required
def team_service_overview(service_id):
    service = Service.query.get(service_id)
    if service and current_user.team.id == service.team_id:
        return render_services_page('services/service.html',
                                    service=service,
                                    team=current_user.team)
    return "no."

@mod_services.route('/<service_id>/check/<check_id>', methods=['GET', 'POST'])
@login_required
def team_service_check_overview(service_id, check_id):
    service = Service.query.get(service_id)
    check = ServiceCheck.query.get(check_id)
    if service and check and check in service.checks and current_user.team.id == service.team_id:
        return render_services_page('services/check.html',
                                    service=service,
                                    check=check,
                                    team=current_user.team)
    return "no."

@mod_services.route('/<service_id>/cred/<credential_id>', methods=['GET', 'POST'])
@login_required
def team_service_credentials_overview(service_id, credential_id):
    service = Service.query.get(service_id)
    credential = CheckCredentials.query.get(credential_id)

    if credential.service == service and service.team_id == current_user.team.id:
        return render_services_page('services/credential.html')

    return "no."
