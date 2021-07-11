from flask import Blueprint, render_template, request, Flask, redirect, url_for, make_response, session
from forms import LoginForm, SignupForm
import hashlib
from markupsafe import escape

home = Blueprint('home', __name__)


@home.route('/home')
@home.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html', title='Home')


@home.route('/chi-siamo')
def about():
    return render_template('about.html', title='Chi siamo')


@home.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        result = request.form
        username = result['username']
        password = hashlib.sha256(result['password'].encode()).hexdigest()
        # if user.password == password: se la password combacia con il db
        # controllare se i dati corrispondono a quelli del DB
        # settare cookie di sessione, query deve ritornare l'id dell'utente
        iduser = 0  # facciamo finta sia id dell'utente restituita in query
        session['iduser'] = iduser
        session['username'] = username
        resp = make_response(redirect(url_for('home.myaccount')))  # mando a my-account dopo login
        resp.set_cookie('loggato', str(iduser))
        return resp
        # altrimenti return 'credenziali sbagliate'
    return render_template('login.html', title='Login', form=form)


@home.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.is_submitted():
        result = request.form
        username = result['username']
        password = hashlib.sha256(result['password'].encode()).hexdigest()
        mail = result['email']
        # mettere i campi nella tabella degli utenti
    return render_template('signup.html', title='Signup', form=form)


@home.route('/my-survey')
def mysurvey():
    return render_template('my-survey.html', title='Survey')


@home.route('/my-account')
def myaccount():
    try:
        username = escape(session['username'])
        return render_template('my-account.html', title='My Account', username=username)
    except:
        return render_template('my-account.html', title='My Account')
