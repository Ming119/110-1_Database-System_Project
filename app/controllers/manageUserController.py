from datetime import date
from app.models.manageUserAdm import load_all_users, load_user_date 
from util import db;
# from app.models import User;
from flask import session, render_template, redirect, url_for;

def manageUsers(user_id):
    users = load_all_users()
    return render_template("manageUser.html", userlist=users)
    
def show_date(create_at):
    user_date = load_user_date()
    return render_template("manageUser.html", userdatelist=user_date)
