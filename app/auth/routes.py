from flask import Blueprint, render_template, redirect, url_for, flash
from app.auth.forms import RegistrationForm, LoginForm
from app import db
from app.models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('en/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('en/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

######################################################
##              Hebrew Routes                      ##
######################################################

@auth.route('/register', methods=['GET', 'POST'], endpoint='register_he')
def register_he():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login_he'))
    return render_template('he/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'], endpoint='login_he')
def login_he():
    print("Entering login_he route")
    form = LoginForm()
    if form.validate_on_submit():
        print("Form validated successfully")
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            print("Invalid email or password")
            flash('דוא"ל או סיסמה לא תקינים', 'danger')
            return redirect(url_for('auth.login_he'))
        login_user(user, remember=form.remember_me.data)
        flash('ברוך הבא, {}'.format(user.username), 'success')
        print("User logged in successfully")
        return redirect(url_for('main.index'))
    else:
        print("Form validation failed")
        print(form.errors)
    return render_template('he/login.html', form=form)



@auth.route('/logout', endpoint='logout_he')
@login_required
def logout_he():
    logout_user()
    return redirect(url_for('main.index'))