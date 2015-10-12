from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, NumberRange


class InjectApprovalForm(Form):
    value = StringField('Approved Value', validators=[DataRequired()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        try:
            int(self.value.data)
            return True
        except ValueError:
            self.value.errors.append('Value must be numeric.')
            return False
