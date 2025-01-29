import os
from werkzeug.utils import secure_filename 
from flask import current_app, Blueprint, render_template, redirect, url_for, flash, request 
from flask_login import current_user, login_required # Add this import 
from app import db 
from app.models import Post, Milestone, Family, User 
from app.auth.forms import ArticleForm, ChangePasswordForm, AssignFamilyForm
from app.utils import gregorian_to_hebrew

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', endpoint='index')
def index():
    print("Index route reached")
    try:
        return render_template('en/index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e)

@main.route('/dashboard', endpoint='dashboard')
def dashboard():
    try:
        return render_template('en/dashboard.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e)
    
@main.route('/article/<int:post_id>', endpoint='article') 
def article(post_id): 
    post = Post.query.get_or_404(post_id) 
    return render_template('en/article.html', post=post)    
    
@main.route('/articles', endpoint='articles')
def articles():
    try:
        families = Family.query.all()  # Fetch all families
        return render_template('en/articles.html', families=families)  # Pass families to the template
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e)

@main.route('/create_article', methods=['GET', 'POST'], endpoint='create_article')
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
    
    return render_template('en/create_article.html', form=form)

@main.route('/edit_article/<int:post_id>', methods=['GET', 'POST'], endpoint='edit_article')
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
            if milestone_form['title'] and milestone_form['content']:
                milestone = Milestone.query.filter_by(post_id=post.id, title=milestone_form['title']).first()
                if milestone:
                    milestone.content = milestone_form['content']
                    milestone.order = milestone_form['order']  # Update order
                    if milestone_form['image']:
                        filename = secure_filename(milestone_form['image'].filename)
                        image_path = os.path.join(current_app.root_path, 'static/images', filename)
                        milestone_form['image'].save(image_path)
                        milestone.image_path = 'images/' + filename
                else:
                    new_milestone = Milestone(
                        title=milestone_form['title'],
                        content=milestone_form['content'],
                        post=post,
                        order=milestone_form['order']  # Set order for new milestone
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
        milestones = Milestone.query.filter_by(post_id=post.id).order_by(Milestone.order).all()
        for milestone in milestones:
            form.milestones.append_entry({
                'title': milestone.title,
                'content': milestone.content,
                'image': None,
                'order': milestone.order
            })

    return render_template('en/edit_article.html', form=form, post=post)

@main.route('/users', methods=['GET', 'POST'], endpoint='users')
@login_required
def users():
    users = User.query.all()
    families = Family.query.all()
    form = AssignFamilyForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        family_id = form.family_id.data
        user = User.query.get(user_id)
        family = Family.query.get(family_id)
        user.families.append(family)
        db.session.commit()
        flash(f'Assigned family {family.name} to user {user.username}.', 'success')
        return redirect(url_for('main.users'))
    return render_template('en/users.html', users=users, families=families, form=form)

@main.route('/user', methods=['GET', 'POST'], endpoint='user')
@login_required
def user():
    user = current_user
    families = Family.query.order_by(Family.name).all()
    assign_family_form = AssignFamilyForm()
    change_password_form = ChangePasswordForm()

    # Populate the family choices for the assign_family_form
    assign_family_form.family_ids.choices = [(family.id, family.name) for family in families]

    # Set the user_id in the form
    assign_family_form.user_id.data = user.id

    if assign_family_form.validate_on_submit() and 'assign_family' in request.form:
        family_ids = assign_family_form.family_ids.data
        for family_id in family_ids:
            family = Family.query.get(int(family_id))  # Ensure family_id is an integer
            if family not in user.families:
                user.families.append(family)
        db.session.commit()
        flash(f'Assigned selected families to you.', 'success')
        return redirect(url_for('main.user'))

    if change_password_form.validate_on_submit() and 'change_password' in request.form:
        if user.check_password(change_password_form.current_password.data):
            user.set_password(change_password_form.new_password.data)
            db.session.commit()
            flash('Your password has been changed.', 'success')
            return redirect(url_for('main.user'))
        else:
            flash('Current password is incorrect.', 'danger')

    return render_template('en/user.html', user=user, families=families, assign_family_form=assign_family_form, change_password_form=change_password_form)



@main.route('/search', methods=['GET'], endpoint='search')
def search():
    query = request.args.get('query')
    if query:
        results = Post.query.filter(Post.title.contains(query)).all()  # Example search on Post titles
    else:
        results = []
    return render_template('en/search_results.html', query=query, results=results)


@main.route('/about', endpoint='about') 
def about(): 
    try: 
        return render_template('en/about.html') 
    except Exception as e: 
        print(f"Error rendering template: {e}") 
        return str(e) 
    
@main.route('/contact', endpoint='contact') 
def contact(): 
    try: 
        return render_template('en/contact.html') 
    except Exception as e: 
        print(f"Error rendering template: {e}") 
        return str(e)
    
@main.route('/change_password', methods=['GET', 'POST'], endpoint='change_password')
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if user.check_password(form.current_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been changed.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Current password is incorrect.', 'danger')
    return render_template('en/change_password.html', form=form)
###########################################################
#                  Hebrew routes
###########################################################

@main.route('/he', endpoint='index_he')
def index():
    print("Index route reached")
    try:
        return render_template('he/index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e)

@main.route('/he/dashboard', endpoint='dashboard_he')
def dashboard():
    try:
        return render_template('he/dashboard.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e)
    
@main.route('/he/article/<int:post_id>', endpoint='article_he') 
def article(post_id): 
    post = Post.query.get_or_404(post_id) 
    return render_template('he/article.html', post=post)    
    
@main.route('/he/articles', endpoint='articles_he')
def articles():
    try:
        families = Family.query.all()  # Fetch all families
        return render_template('he/articles.html', families=families)  # Pass families to the template
    except Exception as e:
        print(f"Error rendering template: {e}")
        return str(e)

@main.route('/he/create_article', methods=['GET', 'POST'], endpoint='create_article_he')
@login_required
def create_article():
    if current_user.role != 'author':
        flash('You do not have permission to create an article.', 'danger')
        return redirect(url_for('main.index_he'))

    form = ArticleForm()
    form.family_id.choices = [(0, 'בחר משפחה קיימת')] + [(family.id, family.name_he) for family in Family.query.all()]
    
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
    
    return render_template('he/create_article.html', form=form)

@main.route('/he/edit_article/<int:post_id>', methods=['GET', 'POST'], endpoint='edit_article_he')
@login_required
def edit_article_he(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.role != 'author' or post.author != current_user:
        flash('אין לך הרשאה לערוך מאמר זה.', 'סַכָּנָה')
        return redirect(url_for('main.index'))

    form = ArticleForm()
    form.family_id.choices = [(0, 'בחר משפחה קיימת')] + [(family.id, family.name_he) for family in Family.query.all()]
    
    if form.validate_on_submit():
        if form.new_family_name_he.data:
            # Add a new family if provided
            new_family = Family(name=form.new_family_name_he.data)
            db.session.add(new_family)
            db.session.commit()
            post.family_id = new_family.id
        else:
            # Use the selected family
            post.family_id = form.family_id.data

        post.title_he = form.title_he.data
        post.gregorian_death_date = form.gregorian_death_date.data
        hebrew_year, hebrew_month, hebrew_day = gregorian_to_hebrew(post.gregorian_death_date)
        post.hebrew_year = hebrew_year
        post.hebrew_month = hebrew_month
        post.hebrew_day = hebrew_day

        db.session.commit()

        for milestone_form in form.milestones.data:
            if milestone_form['title'] and milestone_form['content']:
                milestone = Milestone.query.filter_by(post_id=post.id, title_he=milestone_form['title_he']).first()
                if milestone:
                    milestone.content_he = milestone_form['content_he']
                    milestone.order = milestone_form['order']  # Update order
                    if milestone_form['image']:
                        filename = secure_filename(milestone_form['image'].filename)
                        image_path = os.path.join(current_app.root_path, 'static/images', filename)
                        milestone_form['image'].save(image_path)
                        milestone.image_path = 'images/' + filename
                else:
                    new_milestone = Milestone(
                        title_he=milestone_form['title_he'],
                        content_he=milestone_form['content_he'],
                        post=post,
                        order=milestone_form['order']  # Set order for new milestone
                    )
                    if milestone_form['image']:
                        filename = secure_filename(milestone_form['image'].filename)
                        image_path = os.path.join(current_app.root_path, 'static/images', filename)
                        milestone_form['image'].save(image_path)
                        new_milestone.image_path = 'images/' + filename
                    db.session.add(new_milestone)

        db.session.commit()
        flash('המאמר שלך עודכן!', 'הַצלָחָה')
        return redirect(url_for('main.article', post_id=post.id))
    elif request.method == 'GET':
        form.title_he.data = post.title_he
        form.gregorian_death_date.data = post.gregorian_death_date
        if post.family:
            form.family_id.data = post.family.id
        milestones = Milestone.query.filter_by(post_id=post.id).order_by(Milestone.order).all()
        for milestone in milestones:
            form.milestones.append_entry({
                'title_he': milestone.title_he,
                'content_he': milestone.content_he,
                'image': None,
                'order': milestone.order
            })

    return render_template('he/edit_article.html', form=form, post=post)

@main.route('/he/users', methods=['GET', 'POST'], endpoint='users_he')
@login_required
def users():
    users = User.query.all()
    families = Family.query.all()
    form = AssignFamilyForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        family_id = form.family_id.data
        user = User.query.get(user_id)
        family = Family.query.get(family_id)
        user.families.append(family)
        db.session.commit()
        flash(f'משפחה שהוקצתה {family.name} למשתמש {user.username}.', 'הַצלָחָה')
        return redirect(url_for('main.users'))
    return render_template('he/users.html', users=users, families=families, form=form)

@main.route('/he/user', methods=['GET', 'POST'], endpoint='user_he')
@login_required
def user():
    user = current_user
    families = Family.query.order_by(Family.name).all()
    assign_family_form = AssignFamilyForm()
    change_password_form = ChangePasswordForm()

    # Populate the family choices for the assign_family_form
    assign_family_form.family_ids.choices = [(family.id, family.name_he) for family in families]

    # Set the user_id in the form
    assign_family_form.user_id.data = user.id

    if assign_family_form.validate_on_submit() and 'assign_family' in request.form:
        family_ids = assign_family_form.family_ids.data
        for family_id in family_ids:
            family = Family.query.get(int(family_id))  # Ensure family_id is an integer
            if family not in user.families:
                user.families.append(family)
        db.session.commit()
        flash(f'הקצה לך משפחות נבחרות.', 'הַצלָחָה')
        return redirect(url_for('main.user'))

    if change_password_form.validate_on_submit() and 'change_password' in request.form:
        if user.check_password(change_password_form.current_password.data):
            user.set_password(change_password_form.new_password.data)
            db.session.commit()
            flash('הסיסמה שלך שונתה.', 'הַצלָחָה')
            return redirect(url_for('main.user'))
        else:
            flash('הסיסמה הנוכחית שגויה.', 'סַכָּנָה')

    return render_template('he/user.html', user=user, families=families, assign_family_form=assign_family_form, change_password_form=change_password_form)

@main.route('/he/search', methods=['GET'], endpoint='search_he')
def search():
    query = request.args.get('query')
    if query:
        results = Post.query.filter(Post.title.contains(query)).all()  # Example search on Post titles
    else:
        results = []
    return render_template('he/search_results.html', query=query, results=results)


@main.route('/he/about', endpoint='about_he') 
def about(): 
    try: 
        return render_template('he/about.html') 
    except Exception as e: 
        print(f"Error rendering template: {e}") 
        return str(e) 
    
@main.route('/he/contact', endpoint='contact_he') 
def contact(): 
    try: 
        return render_template('he/contact.html') 
    except Exception as e: 
        print(f"Error rendering template: {e}") 
        return str(e)
    
@main.route('/he/change_password', methods=['GET', 'POST'], endpoint='change_password_he')
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if user.check_password(form.current_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('הסיסמה שלך שונתה.', 'הַצלָחָה')
            return redirect(url_for('main.index'))
        else:
            flash('הסיסמה הנוכחית שגויה.', 'סַכָּנָה')
    return render_template('he/change_password.html', form=form)


    
