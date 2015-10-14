from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class ProfileForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    display_name = StringField('Display Name')

    def __init__(self, user):
        self.first_name.data = user.first_name
        self.last_name.data = user.last_name
        self.display_name.data = user.display_name
        Form.__init__(self)
