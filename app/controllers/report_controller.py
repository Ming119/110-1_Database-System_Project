from app.models import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



@login_required
def index():
    return render_template('report/index.html')
