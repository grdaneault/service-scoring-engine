# Import flask dependencies
from flask import abort, Blueprint, redirect, url_for, render_template, flash

# Import the database object from the main app module
from flask.ext.login import current_user, login_required
from checks import ServiceCheck, CheckCredentials
from checks.services import Service
from scoreboard.app import db, flash_errors
from scoreboard.credentials.forms import PasswordChangeForm

mod_credentials = Blueprint('credentials', __name__, url_prefix='/credentials')

def render_credentials_page(*args, **kwargs):
    kwargs['active_menu'] = 'credentials'
    return render_template(*args, **kwargs)

@mod_credentials.route('/', methods=['GET'])
@login_required
def team_credentials_list():
    team = current_user.team
    credentials = team.credentials

    return render_credentials_page('credentials/index.html',
                                   team=team,
                                   credentials=credentials)


@mod_credentials.route('/edit/<credential_id>', methods=['GET', 'POST'])
@login_required
def team_credential_edit(credential_id):
    team = current_user.team
    credential = CheckCredentials.query.get(credential_id)
    if credential is None or credential.team_id != team.id:
        abort(401)

    form = PasswordChangeForm(credential)

    if form.validate_on_submit():
        credential.change_password(form.new_password.data)
        db.session.commit()
        return redirect(url_for('credentials.team_credentials_list'))
    else:
        flash_errors(form)

    return render_credentials_page('credentials/edit.html',
                                   form=form,
                                   team=team,
                                   credential=credential)