from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required


# index page of the MMS
# GET method to render the index page
# POST is not supported
@login_required
def index():
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    searchForm = SearchForm()
    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        users_list = list()
        for word in words:
            users_list.extend(User.query.filter(User.email.contains(word)).all())
            users_list.extend(User.query.filter(User.username.contains(word)).all())
            users_list.extend(User.query.filter(User.first_name.contains(word)).all())
            users_list.extend(User.query.filter(User.last_name.contains(word)).all())

        users = set(users_list)

    else: users = User.getAll()

    userCount = {'all': User.count(),
                    'admin': User.count('admin'),
                    'staff': User.count('staff'),
                    'customer': User.count('customer'),
                }

    return render_template("manageUser.html", users=users, userCount=userCount, searchForm=searchForm)



@login_required
def filterIndex(role):
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))


    searchForm = SearchForm()
    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        users_list = list()
        for word in words:
            users_list.extend(User.query.filter(User.email.contains(word), User.role==role).all())
            users_list.extend(User.query.filter(User.username.contains(word), User.role==role).all())
            users_list.extend(User.query.filter(User.first_name.contains(word), User.role==role).all())
            users_list.extend(User.query.filter(User.last_name.contains(word), User.role==role).all())

        users = set(users_list)

    else: users = User.getByRole(role)

    userCount = {'all': User.count(),
                    'admin': User.count('admin'),
                    'staff': User.count('staff'),
                    'customer': User.count('customer'),
                }

    return render_template("manageUser.html",
                            searchForm=searchForm,
                            users=users,
                            userCount=userCount,
                            filter=role
                        )



# create a new user
# GET method to render the creation page
#   :param: role
# POST method to submit the creation form
@login_required
def create(role):
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

        if newUserForm.role == 'staff':
            if (Staff.create(
                    username   = newUserForm.username.data,
                    email      = newUserForm.email.data,
                    password   = newUserForm.password.data,
                    first_name = newUserForm.first_name.data,
                    last_name  = newUserForm.last_name.data,
                )):
                flash(f'Staff created successfully!', 'success')

            else:
                flash(f'Error creating staff', 'warning')

        elif newUserForm.role == 'customer':
            if (Customer.create(
                    username   = newUserForm.username.data,
                    email      = newUserForm.email.data,
                    password   = newUserForm.password.data,
                    first_name = newUserForm.first_name.data,
                    last_name  = newUserForm.last_name.data,
                    DOB        = newUserForm.DOB.data,
                    is_active    = True
                )):
                flash(f'Customer created successfully!', 'success')

            else:
                flash(f'Error creating customer', 'warning')

        else: flash(f'Error occurred when creating new user', 'warning')

        return redirect(url_for('user.index'))

    return render_template("newUser.html", newUserForm=newUserForm)



# details page of the user profile
# GET method to render the user profile
#   :param: user_id
# POST method is not supported
@login_required
def profile(user_id):
    if current_user.role != 'admin' and current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    user = User.getByID(user_id)
    return render_template("userProfile.html", user=user)



# update user profile
# GET method to render the update profile page
#   :param: user_id
# POST method to submit the update profile form
@login_required
def update(user_id):
    if current_user.role != 'admin' and current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    updateProfileForm = UpdateProfileForm();
    user = User.getByID(user_id)

    if request.method == 'POST' and updateProfileForm.validate_on_submit():
        if (user.update(
                username   = updateProfileForm.username.data,
                first_name = updateProfileForm.first_name.data,
                last_name  = updateProfileForm.last_name.data
        )):
            flash(f'Profile updated successfully', 'success');

        else:
            flash(f'Error updating profile', 'warning')

        return redirect(url_for('user.profile', user_id=user_id))

    updateProfileForm.username.data = user.username
    updateProfileForm.first_name.data = user.first_name
    updateProfileForm.last_name.data = user.last_name

    return render_template("updateProfile.html",
                user              = user,
                updateProfileForm = updateProfileForm
            );



def changePassword(user_id):
    if current_user.role != 'admin' and current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    form = ResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.getByID(user_id)
        if user.changePassword(form.password):
            flash(f'Password changed', 'success')

        else:
            flash(f'Change password failed', 'warning')

        return redirect(url_for('user.profile', user_id=user.user_id))

    return render_template("resetPassword.html", form=form)

# activate an user
# GET method to activate the user
#   :param: user_id
# POST method is not supported
@login_required
def activate(user_id):
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if current_user.activateUserByID(user_id):
        flash(f'Activate profile was successful.', 'success')

    else:
        flash(f'Activate profile failed.', 'warning')

    return redirect(url_for('user.index'))



# deactivate an user
# GET method to deactivate the user
#   :param: user_id
# POST method is not supported
@login_required
def deactivate(user_id):
    if current_user.role != 'admin':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if current_user.deactivateUserByID(user_id):
        flash(f'Deactivate profile was successful.', 'success')

    else:
        flash(f'Deactivate profile failed.', 'warning')

    return redirect(url_for('user.index'))
