from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class NPCForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    race = StringField('Race', validators=[DataRequired()])
    class_type = StringField('Class', validators=[DataRequired()])
    alignment = SelectField('Alignment', choices=[('lawful good', 'Lawful Good'), ('neutral', 'Neutral'), ('chaotic evil', 'Chaotic Evil')], validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class EncounterForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    difficulty = SelectField('Difficulty', choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class CampaignForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    setting = StringField('Setting')
    submit = SubmitField('Submit')
