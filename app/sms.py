import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

def envoyer_sms(telephone, message):
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=telephone
        )
        print(f"SMS envoye a {telephone}: {msg.sid}")
        return True
    except Exception as e:
        print(f"Erreur SMS: {e}")
        return False

def envoyer_alerte_meteo(telephone, ville, alertes):
    if not alertes:
        return False
    message = f"ALERTE AGRICOLE - {ville}:\n"
    for a in alertes:
        message += f"- {a['message']}\n"
    message += "Votre Assistant Agricole BF"
    return envoyer_sms(telephone, message)

def envoyer_alerte_plantation(telephone, province, cultures):
    message = f"RAPPEL PLANTATION - {province}:\n"
    for c, p in cultures.items():
        message += f"- {c}: {p}\n"
    message += "Votre Assistant Agricole BF"
    return envoyer_sms(telephone, message)

def envoyer_alerte_maladie(telephone, culture, maladie):
    message = f"ALERTE MALADIE:\n"
    message += f"Risque de {maladie} sur {culture}.\n"
    message += "Consultez votre agent agricole.\n"
    message += "Votre Assistant Agricole BF"
    return envoyer_sms(telephone, message)

def notifier_tous_utilisateurs(alertes_meteo, ville):
    from app.database import get_db
    if not alertes_meteo:
        return
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT telephone FROM utilisateurs WHERE alertes_sms = 1 AND telephone IS NOT NULL AND telephone != ''"
    )
    utilisateurs = cursor.fetchall()
    conn.close()
    for user in utilisateurs:
        envoyer_alerte_meteo(user['telephone'], ville, alertes_meteo)
