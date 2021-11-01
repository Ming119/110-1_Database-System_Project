from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user, current_user, login_required, logout_user
from app.models import User


@login_required
def manageUsers(user_id):
    users = User.User.query.all()

    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')

    else:
        return render_template("manageUser.html", userlist=users)
