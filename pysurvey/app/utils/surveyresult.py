from app.model import db, Domande, RisposteUtenti, Risposte
from sqlalchemy import func


def takeResults(idSurvey):
    return db.session.query(func.count(RisposteUtenti.idRisposta), Risposte.risposta, Domande.idDomanda,
                            Domande.question, Risposte.idRisposta) \
        .select_from(RisposteUtenti) \
        .join(Risposte, RisposteUtenti.idRisposta == Risposte.idRisposta) \
        .join(Domande, Domande.idDomanda == RisposteUtenti.idDomanda) \
        .filter(Domande.idSurvey == idSurvey) \
        .group_by(Domande.idDomanda, Risposte.risposta, Domande.question, Risposte.idRisposta).all()

def ritornaSurvey(idSurvey):
    # questa funzione ritorna tutte le domande e tutte le risposte necessarie per un quiz
    # è necessario mandare come paramentro l'id della survey

    domandeERisposte = db.session.query(Domande.question.distinct().label('question'), Risposte.risposta,
                                        Domande.idDomanda, Risposte.idRisposta, Domande.singola) \
        .join(Risposte, Domande.idDomanda == Risposte.idDomanda) \
        .filter(Domande.idSurvey == idSurvey).all()
    return domandeERisposte
