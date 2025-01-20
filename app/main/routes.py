from flask import Blueprint, render_template

main = Blueprint('main', __name__)

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
