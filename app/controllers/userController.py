from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models.User import User

@login_required
def manageUsers():
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    else:
        users = User.getAll()
        return render_template("manageUser.html", users=users)

@login_required
def profile(user_id):
    if current_user.role != 'admin' and current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    user = User.getByUserID(user_id)
    return render_template("userProfile.html", user=user)

@login_required
def deleteProfile(user_id):
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if Admin.deleteUserByUserID(user_id):
        flash(f'Delete profile was successful.', 'success')
    else:
        flash(f'Delete profile failed.', 'warning')

    return redirect(url_for('user.manageUsers'))
