import os
from werkzeug.utils import secure_filename 
from flask import current_app, Blueprint, render_template, redirect, url_for, flash, request 
from flask_login import current_user, login_required # Add this import 
from app import db 
from app.models import Post, Milestone, Family 
from app.auth.forms import ArticleForm
from app.utils import gregorian_to_hebrew

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
        families = Family.query.all()  # Fetch all families
        return render_template('articles.html', families=families)  # Pass families to the template
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
    form.family_id.choices = [(0, 'Select an existing family')] + [(family.id, family.name) for family in Family.query.all()]
    
    if form.validate_on_submit():
        if form.new_family_name.data:
            # Add a new family if provided
            new_family = Family(name=form.new_family_name.data)
            db.session.add(new_family)
            db.session.commit()
            family_id = new_family.id
        else:
            # Use the selected family
            family_id = form.family_id.data

        gregorian_death_date = form.gregorian_death_date.data
        hebrew_year, hebrew_month, hebrew_day = gregorian_to_hebrew(gregorian_death_date)
        
        post = Post(
            title=form.title.data,
            gregorian_death_date=gregorian_death_date,
            hebrew_year=hebrew_year,
            hebrew_month=hebrew_month,
            hebrew_day=hebrew_day,
            family_id=family_id,
            author=current_user
        )
        
        db.session.add(post)
        db.session.commit()
        
        for milestone_form in form.milestones.data:
            milestone = Milestone(
                title=milestone_form['title'],
                content=milestone_form['content'],
                post=post
            )
            if milestone_form['image']:
                filename = secure_filename(milestone_form['image'].filename)
                image_path = os.path.join(current_app.root_path, 'static/images', filename)
                milestone_form['image'].save(image_path)
                milestone.image_path = 'images/' + filename
                
            db.session.add(milestone)
        
        db.session.commit()
        flash('Your article has been published!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('create_article.html', form=form)

@main.route('/edit_article/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_article(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.role != 'author' or post.author != current_user:
        flash('You do not have permission to edit this article.', 'danger')
        return redirect(url_for('main.index'))

    form = ArticleForm()
    form.family_id.choices = [(0, 'Select an existing family')] + [(family.id, family.name) for family in Family.query.all()]
    
    if form.validate_on_submit():
        if form.new_family_name.data:
            # Add a new family if provided
            new_family = Family(name=form.new_family_name.data)
            db.session.add(new_family)
            db.session.commit()
            post.family_id = new_family.id
        else:
            # Use the selected family
            post.family_id = form.family_id.data

        post.title = form.title.data
        post.gregorian_death_date = form.gregorian_death_date.data
        hebrew_year, hebrew_month, hebrew_day = gregorian_to_hebrew(post.gregorian_death_date)
        post.hebrew_year = hebrew_year
        post.hebrew_month = hebrew_month
        post.hebrew_day = hebrew_day

        db.session.commit()

        for milestone_form in form.milestones.data:
            milestone = Milestone.query.filter_by(post_id=post.id, title=milestone_form['title']).first()
            if milestone:
                milestone.content = milestone_form['content']
                if milestone_form['image']:
                    filename = secure_filename(milestone_form['image'].filename)
                    image_path = os.path.join(current_app.root_path, 'static/images', filename)
                    milestone_form['image'].save(image_path)
                    milestone.image_path = 'images/' + filename
            else:
                new_milestone = Milestone(
                    title=milestone_form['title'],
                    content=milestone_form['content'],
                    post=post
                )
                if milestone_form['image']:
                    filename = secure_filename(milestone_form['image'].filename)
                    image_path = os.path.join(current_app.root_path, 'static/images', filename)
                    milestone_form['image'].save(image_path)
                    new_milestone.image_path = 'images/' + filename
                db.session.add(new_milestone)

        db.session.commit()
        flash('Your article has been updated!', 'success')
        return redirect(url_for('main.article', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.gregorian_death_date.data = post.gregorian_death_date
        if post.family:
            form.family_id.data = post.family.id
        milestones = Milestone.query.filter_by(post_id=post.id).all()
        for milestone in milestones:
            form.milestones.append_entry({
                'title': milestone.title,
                'content': milestone.content,
                'image': None
            })

    return render_template('edit_article.html', form=form, post=post)

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


