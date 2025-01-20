from flask import Blueprint, render_template

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
