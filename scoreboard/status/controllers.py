# Import flask dependencies
from flask import Blueprint, render_template

# Import the database object from the main app module
from sqlalchemy import null
from checks import CheckRound

mod_status = Blueprint('status', __name__)

@mod_status.route('/', methods=['GET'])
def main_status_page():
    check_round = CheckRound.query.order_by(CheckRound.id.desc()).filter(CheckRound.end.isnot(null())).limit(1).first()
    for team_round in check_round.team_checks:
        for service_round in team_round.service_results:
            if service_round.get_service_score() == 0:
                service_round.check_icon = 'times-circle'
                service_round.status = 'fail'
            elif service_round.get_service_score() == service_round.get_maximum_service_score():
                service_round.check_icon = 'check-circle'
                service_round.status = 'pass'
            else:
                service_round.check_icon = 'exclamation-circle'
                service_round.status = 'warn'

    return render_template('status/index.html', active_menu='dashboard', check_round=check_round)
