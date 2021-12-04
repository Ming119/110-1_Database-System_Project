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
        users = User.getAll()
        return render_template("manageUser.html", users=users)

    return render_template("newUser.html", newUserForm=newUserForm)



@login_required
def createUser(role):
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))



    if role == 'staff':
        newUserForm = NewStaffForm()

    elif role == 'customer':
        newUserForm = NewCustomerForm()



    if request.method == 'POST' and newUserForm.validate_on_submit():
        # check that the username is used
        userCheck = User.getByUsername(newUserForm.username.data)
        if userCheck:
            flash(f'This username ({newUserForm.username.data}) is already exist', 'warning')
            return redirect(url_for('user.index'))

        # check that the email is used
        userCheck = User.getByEmail(newUserForm.email.data)
        if userCheck:
            flash(f'This email ({newUserForm.email.data}) address is already exist', 'warning')
            return redirect(url_for('user.index'))

        elif newUserForm.role == 'staff':
            staff = Staff.create(
                        username   = newUserForm.username.data,
                        email      = newUserForm.email.data,
                        password   = newUserForm.password.data,
                        first_name = newUserForm.first_name.data,
                        last_name  = newUserForm.last_name.data,
                    )
            flash(f'Staff created successfully!', 'success')

        elif newUserForm.role == 'customer':
            customer = Customer.create(
                            username   = newUserForm.username.data,
                            email      = newUserForm.email.data,
                            password   = newUserForm.password.data,
                            first_name = newUserForm.first_name.data,
                            last_name  = newUserForm.last_name.data,
                            DOB        = newUserForm.DOB.data
                        )
            flash(f'Customer created successfully!', 'success')

        else:
            flash(f'Error occurred when creating new user', 'danger')

        return redirect(url_for('user.index'))

    return render_template("newUser.html", newUserForm=newUserForm)



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
