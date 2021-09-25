from app.db import db;
# from app.models import User;
from flask import session, render_template, redirect, url_for;

def profile(uid):
    if session is None:
        return redirect(url_for("/"));
    else:
        return render_template('user.html');
