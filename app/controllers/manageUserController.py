from app.models.manageUserAdm import load_all_users
from util import db;
# from app.models import User;
from flask import session, render_template, redirect, url_for;

def manageUsers(user_id):    
    users = load_all_users()
    return render_template("manageUser.html", userlist=users)