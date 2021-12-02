from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



@login_required
def index():
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    else:
        form = NewUserForm()

        if request.method == 'POST' and form.validate_on_submit():
            createNewUser(form)

        users = User.getAll()
        return render_template("manageUser.html", users=users, form=form)

@login_required
def createNewUser(form):
    userCheck = User.getByUsername(form.username.data)
    if userCheck and userCheck.confirm:
        flash(f'This username ({form.username.data}) is already exist', 'warning')
        return redirect(url_for('index.register'))

    # check that the email is used and confirmed
    userCheck = User.getByEmail(form.email.data)
    if userCheck and userCheck.confirm:
        flash(f'This email ({form.email.data}) address is already exist', 'warning')
        return redirect(url_for('index.register'))

    # TODO: add new user function


    return render_template("manageUser.html", users=users, form=NewUserForm())

@login_required
def profile(user_id):
    if current_user.role != 'admin' and current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    user = User.getByID(user_id)
    return render_template("userProfile.html", user=user)



@login_required
def editProfile(user_id):
    if current_user.role != 'admin' and current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('user.profile', user=user))

    form = EditProfileForm();
    if request.method == 'POST' and form.validate_on_submit():
        # TODO: edit profile function
        raise

    user = User.getByID(user_id)

    return render_template("editProfile.html", user=user, form=form);



@login_required
def deleteProfile(user_id):
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if Admin.deleteUserByID(user_id):
        flash(f'Delete profile was successful.', 'success')

    else:
        flash(f'Delete profile failed.', 'warning')

    return redirect(url_for('user.index'))
