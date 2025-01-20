from flask import Blueprint, render_template, redirect, url_for, flash
from app.auth.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login successful', 'success')
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Registration successful', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
