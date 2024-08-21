from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from ..models import User
from sqlalchemy import func
import datetime

general = Blueprint('general', __name__)

@general.route('/home', methods=['GET'])
def home():     
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return redirect(url_for('general.login'))
        wedding_time = datetime.datetime(year=2025, month=11, day=1, hour=10)
    
    return render_template('home.html', wedding_time=wedding_time, user=current_user, page='home')

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

@general.route('/rsvp', methods=['POST'])
def rsvp():
    if request.method == 'POST':
        rsvpData = request.get_json()
        drink = rsvpData['drink']
        message = rsvpData['message']
        
        print(drink)
        print(message)

    return {}, 201, {'Content-Type': 'application/json'}