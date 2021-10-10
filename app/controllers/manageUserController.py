from util import db;
# from app.models import User;
from flask import session, render_template, redirect, url_for;

def manageUsers(user_id):
    return render_template('manageUser.html');
