from flask import Blueprint, render_template, request, session, url_for, flash, redirect
from flask_login import login_required, logout_user, current_user, login_user
from .models import db, User
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
@auth_bp.route('/signup',methods=["GET","POST"])
def signup():

    if request.method == "GET":
        users = User.query.all()
        return render_template('signup.html',users=users)
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth_bp.signup'))
        
        new_user = User(email=email,name=name,password=generate_password_hash(password, method='sha256'))
        
        db.session.add(new_user)
        db.session.commit()

        
        return redirect(url_for('auth_bp.login'))

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        #create admin upon app creation
        if User.query.all() == '' or User.query.all() == None:
            email = 'johncrowley547@gmail.com'
            name = 'admin'
            password = 'admin'
            admin = True
            our_admin = User(email=email,name=name,password=generate_password_hash(password, method='sha256'),admin=admin)
            db.session.add(our_admin)
            db.session.commit()
            return render_template('login.html')
        else:
            return redirect(url_for('main_bp.index'))
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth_bp.login'))
        
        login_user(user,remember=False)
        return redirect(url_for('main_bp.index'))
        

@auth_bp.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
