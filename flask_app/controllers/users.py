from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def homePage():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login_and_registration.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_users_by_id(data)
        return render_template('successful_login.html', loggedUser= user)
    return redirect('/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route('/create_user', methods=['POST'])
def createUser():
    if not User.validate_user(request.form):
        flash('Somethings wrong!', 'signUp')
        return redirect(request.referrer)
    data = {        
        'email': request.form['email'],
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],        
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.create_user(data)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)
    if not User.get_user_by_email(data):
        flash('This email doesnt exist in this application', 'emailLogin')
        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/dashboard')