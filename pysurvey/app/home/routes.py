from flask import Blueprint, render_template, request, Flask
from forms import LoginForm, SignupForm
import hashlib

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
        # controllare se i dati corrispondono a quelli del DB
        # settare cookie di sessione
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
    return render_template('signup.html', title='Signup')


@home.route('/my-survey')
def mysurvey():
    return render_template('my-survey.html', title='Survey')
