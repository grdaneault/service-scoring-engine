from flask_wtf import Form
from wtforms import StringField, DecimalField
from wtforms.fields.core import LocaleAwareNumberField
from wtforms.validators import DataRequired, NumberRange


class InjectApprovalForm(Form):
    value = DecimalField('Approved Value', validators=[DataRequired()])


class FlagSolveForm(Form):
    flag = StringField('Flag', validators=[DataRequired()])


