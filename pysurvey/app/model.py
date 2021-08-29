from app import app
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
# definizione di tutti i model usati dall'ORM
db = SQLAlchemy(app)  # inizializzazione del db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    immagine = db.Column(db.String(200))
    nazionalita = db.Column(db.String(200), default="Italiana")


class Survey(db.Model):
    idSurvey = db.Column(db.Integer, primary_key=True)  # sono chiavi esterne
    idUser = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    titolo = db.Column(db.String(80), nullable=False)

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
    idSurvey = db.Column(db.Integer, ForeignKey('survey.idSurvey'), nullable=False)  # sono chiavi esterne
    idDomanda = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    singola = db.Column(db.Boolean, nullable=False)


class Risposte(db.Model):
    idRisposta = db.Column(db.Integer, primary_key=True)
    idDomanda = db.Column(db.Integer, ForeignKey('domande.idDomanda'), nullable=False)
    risposta = db.Column(db.String(80), nullable=False)


class RisposteUtenti(db.Model):
    idRisposta = db.Column(db.Integer, ForeignKey('risposte.idRisposta'), nullable=False)
    idDomanda = db.Column(db.Integer, ForeignKey('domande.idDomanda'), nullable=False)
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