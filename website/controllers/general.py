from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from ..models import User
from sqlalchemy import func

general = Blueprint('general', __name__)

@general.route('/home', methods=['GET'])
def home():     
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return redirect(url_for('general.login'))
    
    return render_template('home.html', user=current_user, page='home')

@general.route('/', methods=['GET', 'POST'])
def login():     
    if current_user.is_authenticated:
            return redirect(url_for('general.home'))
    if request.method == 'POST':
        passphrase = request.form.get('passphrase')

        user = User.query.filter(func.lower(User.passphrase) == passphrase.lower()).first()
        
        if user:
            flash('Welcome '+user.name, category='success')
            login_user(user, remember=True)
            return redirect(url_for('general.home'))
        else:
            flash('Passphrase does not exist, try again.', category='error')
    
    return render_template('login.html', user=current_user, page='login')

@general.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('general.login'))