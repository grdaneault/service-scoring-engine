# Import flask dependencies
from flask import Blueprint, render_template

# Import the database object from the main app module
from flask.ext.login import current_user, login_required
from scoreboard.app import db, flash_errors
from scoreboard.users.forms import ProfileForm

mod_users = Blueprint('users', __name__, url_prefix='/users')

def render_credentials_page(*args, **kwargs):
    kwargs['active_menu'] = 'credentials'
    return render_template(*args, **kwargs)

@mod_users.route('/profile/names/edit', methods=['GET', 'POST'])
@login_required
def edit_user_profile_names():

    form = ProfileForm(current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.display_name = form.display_name.data
        db.session.commit()
    else:
        flash_errors(form)

    return render_template('users/profile.html', user=current_user, form=form)
