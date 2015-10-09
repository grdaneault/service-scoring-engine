from flask_wtf import Form
from wtforms import PasswordField
from wtforms.validators import DataRequired


class PasswordChangeForm(Form):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])

    def __init__(self, credential):
        Form.__init__(self)
        self.credential = credential

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if self.old_password.data != self.credential.password:
            self.old_password.errors.append('Incorrect old password')
            return False

        return True