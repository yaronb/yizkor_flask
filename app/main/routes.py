from flask import Blueprint, render_template, redirect, url_for, flash 
from flask_login import current_user, login_required # Add this import 
from app import db 
from app.models import Post 
from app.auth.forms import ArticleForm

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    print("Index route reached")
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e)

@main.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e)
    
@main.route('/articles') 
def articles(): 
    try: 
        return render_template('articles.html') 
    except Exception as e: 
        print(f"Error rendering template: {e}") 
        return str(e) 
@main.route('/about') 
def about(): 
    try: 
        return render_template('about.html') 
    except Exception as e: 
        print(f"Error rendering template: {e}") 
        return str(e) 
    
@main.route('/contact') 
def contact(): 
    try: 
        return render_template('contact.html') 
    except Exception as e: 
        print(f"Error rendering template: {e}") 
        return str(e)
    
@main.route('/create_article', methods=['GET', 'POST']) 
@login_required 
def create_article(): 
    if current_user.role != 'author': 
        flash('You do not have permission to create an article.', 'danger') 
        return redirect(url_for('main.index')) 
    
    form = ArticleForm() 
    if form.validate_on_submit(): 
        post = Post(title=form.title.data, body=form.body.data, author=current_user) 
        db.session.add(post) 
        db.session.commit() 
        flash('Your article has been published!', 'success') 
        return redirect(url_for('main.index')) 
    
    return render_template('create_article.html', form=form)
