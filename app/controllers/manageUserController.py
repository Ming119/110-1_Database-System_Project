from datetime import date
from flask import session, render_template, redirect, url_for
from app.models import User

def manageUsers(user_id):
    users = User.User.query.all()
    return render_template("manageUser.html", userlist=users)

def show_date(create_at):
    user_date = User.User.load_user_date()
    return render_template("manageUser.html", userdatelist=user_date)
