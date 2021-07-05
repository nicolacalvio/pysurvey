from flask import Blueprint, render_template, request, Flask
from forms import SignUpForm
import hashlib

home = Blueprint('home', __name__)

signed_in = 0
#da modificare con un cookie di sessione lato frontend


@home.route('/home')
@home.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html', title='Home') if signed_in == 0 else render_template('home.html', title='Home',
                                                                                             signed_in='True')


@home.route('/chi-siamo')
def about():
    return render_template('about.html', title='Chi siamo') if signed_in == 0 else render_template('about.html', title='Chi siamo',
                                                                                             signed_in='True')


@home.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        username = result['username']
        password = hashlib.sha256(result['password'].encode()).hexdigest()
        #mettere username e password nel db
    return render_template('signup.html', title='Signup', form=form) if signed_in == 0 else render_template('signup.html', title='Signup',
                                                                                             signed_in='True', form=form)


@home.route('/login')
def login():
    return render_template('login.html', title='Login') if signed_in == 0 else render_template('login.html', title='Login',
                                                                                             signed_in='True')

@home.route('/my-survey')
def mysurvey():
    return render_template('my-survey.html', title='Survey')