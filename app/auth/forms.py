from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, DateField, PasswordField, BooleanField, SubmitField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from app.models import User

class MilestoneForm(FlaskForm): 
    title = StringField('Name of Milestone', validators=[DataRequired()]) 
    content = TextAreaField('Content', validators=[DataRequired()]) 
    image = FileField('Image') 

class ArticleForm(FlaskForm):
   title = StringField('Title', validators=[DataRequired()]) 
   gregorian_death_date = DateField('Gregorian Death Date', format='%Y-%m-%d', validators=[DataRequired()]) 
   family_id = SelectField('Family', coerce=int, validators=[Optional()])
   new_family_name = StringField('New Family Name', validators=[Optional()])
   milestones = FieldList(FormField(MilestoneForm), min_entries=1, max_entries=10) 
   submit = SubmitField('Publish')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
