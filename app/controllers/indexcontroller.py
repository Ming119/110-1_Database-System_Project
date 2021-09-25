from app import db;
from flask import flash, redirect, render_template, request, session, url_for;

from forms import RegisterForm, LoginForm;

def index():
    return render_template('index.html');

def register():
    form = RegisterForm.RegisterForm();

    if request.method == 'POST' and form.vavalidate_on_submit():
        user = User(
            username = form.username.data,
            email    = form.email.data,
            password = form.password.data
        );
        db.session.add(user);
        db.session.commit();

        return redirect(url_for('index'));

    return render_template('register.html', form=form);

def login():
    form = LoginForm();

    if request.method == 'POST' and form.vavalidate_on_submit():
        pass;

    return render_template('login.html', form=form);

def logout():
    session.clear();
    return redirect(url_for('index'));
