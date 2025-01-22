from convertdate import hebrew
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from flask_mail import Message
from app import mail

def gregorian_to_hebrew(gregorian_date):
    year, month, day = hebrew.from_gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    return year, month, day

def send_reminder_email(post):
    msg = Message("Yizkor Reminder", sender="your-email@example.com", recipients=[post.author.email])
    msg.body = f"Remembering {post.title} on this day."
    mail.send(msg)

def check_dates_and_send_reminders(db, Post):
    today = date.today()
    hebrew_year, hebrew_month, hebrew_day = gregorian_to_hebrew(today)

    if hebrew_day == 1:  # First day of the Hebrew month
        posts = db.session.query(Post).filter_by(hebrew_month=hebrew_month).all()
        for post in posts:
            send_reminder_email(post)

scheduler = BackgroundScheduler()
