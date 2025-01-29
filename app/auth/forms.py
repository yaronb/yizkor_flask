from flask_wtf import FlaskForm
from wtforms import StringField, FileField, FieldList, FormField, TextAreaField, DateField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User

class MilestoneForm(FlaskForm): 
    title = StringField('Name of Milestone', validators=[DataRequired()]) 
    title_he = StringField('שם אבן דרך', validators=[DataRequired()]) 
    content = TextAreaField('Content', validators=[DataRequired()]) 
    content_he = TextAreaField('תוֹכֶן', validators=[DataRequired()]) 
    image = FileField('Image') 
    order = HiddenField('Order')
    image_he = FileField('תְמוּנָה') 
    

class ArticleForm(FlaskForm):
   title = StringField('Title', validators=[DataRequired()]) 
   title_he = StringField('כותרת', validators=[DataRequired()])
   gregorian_death_date = DateField('Gregorian Death Date', format='%Y-%m-%d', validators=[DataRequired()]) 
   family_id = SelectField('Family', coerce=int, validators=[Optional()])
   new_family_name = StringField('New Family Name', validators=[Optional()])
   milestones = FieldList(FormField(MilestoneForm), min_entries=1, max_entries=10) 
   submit = SubmitField('Publish')
   new_family_name_he = StringField('שם משפחה חדש', validators=[Optional()])
   submit_he = SubmitField('פרסם')   

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
    email_he = StringField('דוא"ל', validators=[DataRequired(), Email()])
    password_he = PasswordField('סיסמה', validators=[DataRequired()])
    remember_me_he = BooleanField('זכור אותי')
    submit_he = SubmitField('התחבר')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    username_he = StringField('שם משתמש', validators=[DataRequired()])
    email_he = StringField('דוא"ל', validators=[DataRequired(), Email()])
    password_he = PasswordField('סיסמה', validators=[DataRequired()])
    password2_he = PasswordField('חזור על הסיסמה', validators=[DataRequired(), EqualTo('password')])
    submit_he = SubmitField('הירשם')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
    current_password_he = PasswordField('סיסמה נוכחית', validators=[DataRequired()])
    new_password_he = PasswordField('סיסמה חדשה', validators=[DataRequired(), Length(min=6)])
    confirm_new_password_he = PasswordField('אשר סיסמה חדשה', validators=[DataRequired(), EqualTo('new_password')])
    submit_he = SubmitField('שנה סיסמה')

class AssignFamilyForm(FlaskForm):
    user_id = HiddenField('User ID', validators=[DataRequired()])
    family_ids = SelectMultipleField('Families', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Family')
    user_id_he = HiddenField('מזהה משתמש', validators=[DataRequired()])
    family_ids_he = SelectMultipleField('משפחות', coerce=int, validators=[DataRequired()])
    submit_he = SubmitField('הקצה משפחה')

