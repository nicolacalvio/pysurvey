from enum import unique

import primary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import TestingConfig, DevelopmentConfig, ProductionConfig
import os
from flask import Blueprint, render_template, request, Flask, redirect, url_for, make_response, session
from flask_wtf import FlaskForm
from forms import LoginForm, SignupForm
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nosql'
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:bitnami@localhost:5432/pysurvey"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    immagine = db.Column(db.String(200))


class Survey(db.Model):
    idSurvey = db.Column(db.Integer, primary_key=True)  # sono chiavi esterne
    idUser = db.Column(db.Integer)
    titolo = db.Column(db.String(80))


class Domande(db.Model):
    idSurvey = db.Column(db.Integer)  # sono chiavi esterne
    idDomanda = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))


class Risposte(db.Model):
    idRisposta = db.Column(db.Integer, primary_key=True)
    idDomanda = db.Column(db.Integer)
    risposta = db.Column(db.String(80))


db.create_all()

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
        password = result['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                # controllare se i dati corrispondono a quelli del DB
                # settare cookie di sessione, query deve ritornare l'id dell'utente
                iduser = user.id  # facciamo finta sia id dell'utente restituita in query
                session['iduser'] = iduser
                session['username'] = username
                session['mail'] = user.email
                session['immagine'] = user.immagine
                resp = make_response(redirect(url_for('home.myaccount')))  # mando a my-account dopo login
                return resp
                # altrimenti return 'credenziali sbagliate'
        return '<h1>username o password errati</h1>'
    return render_template('login.html', title='Login', form=form)


@home.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.is_submitted():
        result = request.form
        username = result['username']
        password = generate_password_hash(result['password'], method='sha256')
        mail = result['email']
        new_user = User(username=username, email=mail, password=password, immagine="../static/img/profile.png")
        db.session.add(new_user)
        db.session.commit()
        iduser = new_user.id  # facciamo finta sia id dell'utente restituita in query
        session['iduser'] = iduser
        session['username'] = username
        session['mail'] = mail
        session['immagine'] = "../static/img/profile.png"
        resp = make_response(redirect(url_for('home.myaccount')))  # mando a my-account dopo login
        return resp
    return render_template('signup.html', title='Signup', form=form)


@home.route('/my-survey')
def mysurvey():
    return render_template('my-survey.html', title='Survey')


@home.route('/my-account')
def myaccount():
    try:
        username = escape(session['username'])
        mail = escape(session['mail'])
        immagine = escape(session['immagine'])
        return render_template('my-account.html', title='MY ACCOUNT', username=username, mail=mail, immagine=immagine)
    except:
        return render_template('my-account.html', title='MY ACCOUNT')


@home.route('/logged')
def isLogged():
    try:
        if session['iduser']:
            return "1"
        return "0"
    except:
        return "0"


app.register_blueprint(home)
