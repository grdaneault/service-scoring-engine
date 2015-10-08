# Import flask dependencies
from flask import Blueprint, render_template

# Import the database object from the main app module
from checks import CheckRound

mod_status = Blueprint('status', __name__)

@mod_status.route('/', methods=['GET'])
def main_status_page():
    rounds = CheckRound.query.order_by(CheckRound.id.desc()).limit(2).all()
    return render_template('status/index.html', active_menu='dashboard', check_rounds=rounds, count=len(rounds))