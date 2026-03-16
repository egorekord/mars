from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Description', validators=[DataRequired()])
    work_size = IntegerField('Hours', validators=[DataRequired()])
    collaborators = StringField('List of id of participants', validators=[DataRequired()])
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    job = StringField('Description', validators=[DataRequired()])
    work_size = IntegerField('Hours', validators=[DataRequired()])
    collaborators = StringField('List of id of participants', validators=[DataRequired()])
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Submit')