import os
from werkzeug.utils import secure_filename 
from flask import current_app, Blueprint, render_template, redirect, url_for, flash 
from flask_login import current_user, login_required # Add this import 
from app import db 
from app.models import Post, Milestone 
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
    
@main.route('/article/<int:post_id>') 
def article(post_id): 
    post = Post.query.get_or_404(post_id) 
    return render_template('article.html', post=post)    
    
@main.route('/articles') 
def articles(): 
    try: 
        posts = Post.query.order_by(Post.publication_date.desc()).all
        return render_template('articles.html', post=posts) 
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
        post = Post(title=form.title.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        
        for milestone_form in form.milestones.data:
            milestone = Milestone(title=milestone_form['title'],
                                  content=milestone_form['content'],
                                  post=post)
            
            if milestone_form['image']:
                filename = secure_filename(milestone_form['image'].filename)
                milestone_form['image'].save(os.path.join(current_app.root_path, 'static', filename))
                milestone.image_path = filename
                
            db.session.add(milestone)
        
        db.session.commit()
        flash('Your article has been published!', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_article.html', form=form)

