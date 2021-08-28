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
from sqlalchemy import func, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.inspection import inspect
import csv

# inizio della configurazione necesaria all'amiente
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nosql'
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:bitnami@pysurvey.ddns.net:5432/pysurvey"
db = SQLAlchemy(app)  # inizializzazione del db


# definizione di tutti i model usati dall'ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    immagine = db.Column(db.String(200))
    nazionalita = db.Column(db.String(200), default="Italiana")


class Survey(db.Model):
    idSurvey = db.Column(db.Integer, primary_key=True)  # sono chiavi esterne
    idUser = db.Column(db.Integer, ForeignKey('user.id'))
    titolo = db.Column(db.String(80))

    # property utile in fase di serializzaizone in json
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'idSurvey': self.idSurvey,
            'idUser': self.idUser,
            'titolo': self.titolo
        }


class Domande(db.Model):
    idSurvey = db.Column(db.Integer, ForeignKey('survey.idSurvey'))  # sono chiavi esterne
    idDomanda = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))


class Risposte(db.Model):
    idRisposta = db.Column(db.Integer, primary_key=True)
    idDomanda = db.Column(db.Integer, ForeignKey('domande.idDomanda'))
    risposta = db.Column(db.String(80))


class RisposteUtenti(db.Model):
    idRisposta = db.Column(db.Integer, ForeignKey('risposte.idRisposta'))
    idDomanda = db.Column(db.Integer, ForeignKey('domande.idDomanda'))
    idUtente = db.Column(db.Integer, ForeignKey('user.id'))
    idRispostaUtente = db.Column(db.Integer, primary_key=True)


class Statistiche:
    # classe nata per modellare la risposta di una query, contiene i campi nel costruttore
    # utile per la serializzazione in oggeto json
    def __init__(self, numeroRisposte, risposta, idDomanda, domanda, idRisposta):
        self.numeroRisposte = numeroRisposte
        self.risposta = risposta
        self.idDomanda = idDomanda
        self.domanda = domanda
        self.idRisposta = idRisposta

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'numeroRisposte': self.numeroRisposte,
            'risposta': self.risposta,
            'idDomanda': self.idDomanda,
            'domanda': self.domanda,
            'idRisposta': self.idRisposta
        }


db.create_all()  # creo tutte le tabelle
home = Blueprint('home', __name__)


@home.route('/home')
@home.route('/', methods=['GET', 'POST'])  # ci si può referenziare alla home in due modi
def homepage():
    return render_template('home.html', title='Home')


@home.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # abbiamo usato flask_wtf per i form
    if form.is_submitted():  # se il form è submittato
        result = request.form
        username = result['username']
        password = result['password']  # prendo i vari campi del form
        user = User.query.filter_by(username=username).first()  # trovo l'user
        if user:
            if check_password_hash(user.password, password):  # se l'user esiste checko la passwordo
                # controllare se i dati corrispondono a quelli del DB
                # settare cookie di sessione
                iduser = user.id
                # setto i cookie di sessione di tipo httpOnly per tenere lo stato dell'utente
                session['iduser'] = iduser
                session['username'] = username
                session['mail'] = user.email
                session['immagine'] = user.immagine
                session['nazionalita'] = user.nazionalita
                resp = make_response(redirect(url_for('home.myaccount')))  # mando a my-account dopo login
                return resp
                # altrimenti return 'credenziali sbagliate'
        return '<h1>username o password errati</h1>'
    return render_template('login.html', title='Login', form=form)


@home.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.is_submitted():  # se il form è inviato
        result = request.form
        username = result['username']  # prendo dati
        password = generate_password_hash(result['password'], method='sha256')  # creo hash sha256
        mail = result['email']
        new_user = User(username=username, email=mail, password=password,
                        immagine="../static/img/profile.png")  # creo utente
        db.session.add(new_user)
        db.session.commit()  # metto in db l'utente
        iduser = new_user.id  # id dell'utente
        # imposto il cookie di sessione
        session['iduser'] = iduser
        session['username'] = username
        session['mail'] = mail
        session['immagine'] = "../static/img/profile.png"
        session['nazionalita'] = "Italiana"
        resp = make_response(redirect(url_for('home.myaccount')))  # mando a my-account dopo signup
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
        nazionalita = escape(session['nazionalita'])
        return render_template('my-account.html', title='MY ACCOUNT', username=username, mail=mail, immagine=immagine,
                               nazionalita=nazionalita)
    except:
        return render_template('my-account.html', title='MY ACCOUNT')


# API time

@home.route('/logged')
def isLogged():
    # questa funzione viene usata come API e dice se l'utente è loggato
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
    # attenzione se l'utente non modifica qualcosa non si mette nella richiesta!
    # l'ordine in cui mettete i paramentri non è importante
    id = escape(session['iduser'])
    user = db.session.query(User).filter(User.id == int(id)).first()
    if 'immagine' in request.args:
        user.immagine = request.args['immagine']
        session['immagine'] = user.immagine
    if 'nome' in request.args:
        user.username = request.args['nome']
        session['username'] = user.username
    if 'mail' in request.args:
        user.email = request.args['mail']
        session['mail'] = user.email
    if 'nazionalita' in request.args:
        user.nazionalita = request.args['nazionalita']
        session['nazionalita'] = user.nazionalita
    db.session.commit()
    return "success"


@home.route('/inviaRisposta', methods=['POST'])
def riceviRisposta():
    # questa funzione salva la risposta di un sondaggio
    content = request.get_json()
    # per ogni domanda mi salvo la risposta, se l'utente è loggato mi salvo in db anche il suo id
    for domanda in content:
        if isLogged() == "1":
            db.session.add(RisposteUtenti(idDomanda=domanda['idDomanda'], idRisposta=domanda['idRisposta'],
                                          idUtente=escape(session['iduser'])))
        else:
            db.session.add(RisposteUtenti(idDomanda=domanda['idDomanda'], idRisposta=domanda['idRisposta']))
        db.session.commit()
    return "success"


def ritornaSurvey(idSurvey):
    # questa funzione ritorna tutte le domande e tutte le risposte necessarie per un quiz
    # è necessario mandare come paramentro l'id della survey

    domandeERisposte = db.session.query(Domande.question.distinct().label('question'), Risposte.risposta,
                                        Domande.idDomanda, Risposte.idRisposta) \
        .join(Risposte, Domande.idDomanda == Risposte.idDomanda) \
        .filter(Domande.idSurvey == idSurvey).all()
    return domandeERisposte


@home.route('/creaSurvey', methods=['POST'])
def creaSurvey():
    # questa funzione accetta in input un json che contiene tutte le risposte
    # e tutte le domande all'interno della survey
    iduser = escape(session['iduser'])
    content = request.get_json()
    nuova_survey = Survey(idUser=iduser, titolo=content['titolo'])  # creo survey nella tabella
    db.session.add(nuova_survey)
    db.session.commit()
    for i in range(len(content) - 2):
        nuova_domanda = Domande(idSurvey=nuova_survey.idSurvey, question=content[str(i)]['domande'])  # aggiungo domanda
        db.session.add(nuova_domanda)
        db.session.commit()
        for j in range(len(content[str(i)]['risposte'])):
            nuova_risposta = Risposte(idDomanda=nuova_domanda.idDomanda, risposta=content[str(i)]['risposte'][str(j)])
            # aggiungo risposta
            db.session.add(nuova_risposta)
            db.session.commit()
    return "success"


@home.route('/titoloEId')
def ritornaTitoloEId():
    # ritorna tutte le domande dell'utente e l'id
    if isLogged() == "1":
        idUtente = escape(session['iduser'])
        titoliEId = db.session.query(Survey).filter(Survey.idUser == idUtente).all()
        if len(titoliEId) > 0:
            return jsonify(json_list=[i.serialize for i in titoliEId])  # ritorno in json tutte le survey dell'utente
        return "Non hai ancora alcuna survey creata. \n Creane subito una!"
    return "Per vedere le tue survey o crearne delle nuove accedi oppure crea un account!"


@home.route('/survey')
def specificaSurvey():
    # questa funzione ritorna la survey (domande e risposte)
    if 'id' in request.args:
        id = request.args['id']
        survey = ritornaSurvey(id)
        return render_template('survey.html', title='SURVEY', survey=survey, len=len(survey))


@home.route('/crea')
def creaSondaggio():
    return render_template('crea_sondaggio.html', title='CREA SURVEY')


@home.route('/ritorna-risultati')
def ritornaRisultati():
    # questa funzione ritorna i risultati di un sondaggio, in particolare
    # numero di risposte alla risposta, domanda a cui si riferisce la risposta
    # accetta come parametro l'id della survey
    if 'id' in request.args:
        idSurvey = int(request.args['id'])
        risp = db.session.query(func.count(RisposteUtenti.idRisposta), Risposte.risposta, Domande.idDomanda,
                                Domande.question, Risposte.idRisposta) \
            .select_from(RisposteUtenti) \
            .join(Risposte, RisposteUtenti.idRisposta == Risposte.idRisposta) \
            .join(Domande, Domande.idDomanda == RisposteUtenti.idDomanda) \
            .filter(Domande.idSurvey == idSurvey) \
            .group_by(Domande.idDomanda, Risposte.risposta, Domande.question, Risposte.idRisposta).all()
        print(risp)
        return jsonify(json_list=[Statistiche(i[0], i[1], i[2], i[3], i[4]).serialize() for i in risp])
    return "fallito"
    # prendere i dati dal db sulla determinata Survey
    # trasformare in json i dati
    # returnarli


@home.route('/csv')
def crea_csv():
    # scarica in formato CSV le statistiche delle survey
    if 'id' in request.args:
        idSurvey = request.args['id']
        l = []
        for r in db.session.query((RisposteUtenti.idRisposta)).filter(
                RisposteUtenti.idDomanda == idSurvey).all():  # manca solo sistemare la query, però il cvs si forma
            # TODO: idDomanda deve diventare l'id della survey in quanto il csv è riasuntivo dell'intera survey non solo di una domanda
            l.append(r)
        with open("f1.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(l)
        return "fatto"
    else:
        return "errore id non presente"


@home.route('/statistiche')
def statistiche():
    if 'id' in request.args:
        idSurvey = request.args['id']
        if isLogged() == "1":
            idUserSurvey = db.session.query(Survey.idUser).filter(Survey.idSurvey == idSurvey).first()[0]
            if int(idUserSurvey) == int(escape(session['iduser'])):
                return render_template('statistiche.html', title='STATISTICHE')
            else:
                return "<h1>Solo il creatore può vedere le statistiche della survey</h1>"
        else:
            return "<h1>Devi essere loggato per vedere le statistiche della survey</h1>"
    return "<h1>Non hai inserito un id valido</h1>"


app.register_blueprint(home)
