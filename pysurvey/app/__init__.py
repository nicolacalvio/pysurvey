from enum import unique

import primary
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import TestingConfig, DevelopmentConfig, ProductionConfig
import os
from flask import Blueprint, render_template, request, Flask, redirect, url_for, make_response, session, jsonify
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


class RisposteUtenti(db.Model):
    idRisposta = db.Column(db.Integer)
    idDomanda = db.Column(db.Integer)
    idUtente = db.Column(db.Integer)
    idRispostaUtente = db.Column(db.Integer, primary_key=True)


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


# API time

@home.route('/logged')
def isLogged():
    # questa funzione dice se l'utente è loggato
    try:
        if session['iduser']:
            return "1"
        return "0"
    except:
        return "0"


@home.route('/modificaAccount', methods=['GET'])
def modifyAccount():
    # questa funzione permette di modificare l'account
    # la richiesta deve essere /modificaAccount?immagine="/img/immagine.png"&nome="nicola"&mail="prova@prova.it"
    # attenzione se l'utente non modifica qualcosa non mettetelo nella richiesta!
    # l'ordine in cui mettete i paramentri non è importante
    id = escape(session['iduser'])
    user = db.session.query(User).filter(User.id == id).first()
    if 'immagine' in request.args:
        user.immagine = request.args['immagine']
    if 'nome' in request.args:
        user.nome = request.args['nome']
    if 'mail' in request.args:
        user.mail = request.args['mail']
    db.session.commit()
    return "success"


@home.route('/inviaRisposta', methods=['POST'])
def riceviRisposta():
    # questa funzione salva la risposta di un sondaggio
    content = request.get_json()
    # json
    # {
    #   [
    #       idDomanda:x,
    #       idRisposta:y
    #   ],
    #   [
    #       idDomanda:x,
    #       idRisposta:y
    #   ]
    # }
    contenuto = json.loads(content)
    for domanda in contenuto:
        if isLogged() == "1":
            db.session.add(RisposteUtenti(idDomanda=['idDomanda'], idRisposta=domanda['idRisposta'],
                                          idUtente=escape(session['iduser'])))
        else:
            db.session.add(RisposteUtenti(idDomanda=['idDomanda'], idRisposta=domanda['idRisposta']))
        db.session.commit()
        return "success"


@home.route('/prendiQuiz', methods=['POST'])
def ritornaQuiz():
    # questa funzione ritorna tutte le domande e tutte le risposte necessarie per un quiz
    # è necessario mandare come paramentro l'id del survey
    if 'idSurvey' in request.args:
        domandeERisposte = db.session.query(Domande.question.distinct().label('question')) \
            .join(Risposte, Domande.idDomanda == Risposte.idDomanda) \
            .addColumn('idSurvey', 'idDomanda', 'question', 'idDomanda', 'idRisposta', 'Risposta') \
            .filter(Domande.idSurvey == request.args['idSurvey'])
        return jsonify(domandeERisposte)
    else:
        return "manca l'id survey"


app.register_blueprint(home)
