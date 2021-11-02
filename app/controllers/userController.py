from flask import session, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import User

def profile(user_id):
    return 'profile'


@login_required
def manageUsers():
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    else:
        users = User.User.query.all()
        return render_template("manageUser.html", userlist=users)
