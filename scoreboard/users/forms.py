from wtforms import StringField, Form
from wtforms.validators import DataRequired


class ProfileForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    display_name = StringField('Last Name', validators=[DataRequired()])