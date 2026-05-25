import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_meteo(ville):
    try:
        params = {
            "q": ville,
            "appid": API_KEY,
            "units": "metric",
            "lang": "fr"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            meteo = {
                "ville": ville,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidite": data["main"]["humidity"],
                "vent": data["wind"]["speed"]
            }
            return meteo
        else:
            return {"erreur": "Ville non trouvée"}

    except Exception as e:
        return {"erreur": str(e)}

def conseil_meteo(ville):
    meteo = get_meteo(ville)

    if "erreur" in meteo:
        return "Je n'ai pas pu récupérer la météo pour cette ville."

    temp = meteo["temperature"]
    humidite = meteo["humidite"]
    description = meteo["description"]

    conseil = f"🌤️ Météo à {ville} : {description}, {temp}°C, humidité {humidite}%.\n"

    if temp > 35:
        conseil += "⚠️ Chaleur excessive ! Arrosez tôt le matin ou le soir."
    elif temp < 15:
        conseil += "🥶 Températures basses. Protégez vos cultures fragiles."
    else:
        conseil += "✅ Températures favorables pour la plupart des cultures."

    if humidite > 80:
        conseil += "\n💧 Humidité élevée. Risque de maladies fongiques, surveillez vos cultures."
    elif humidite < 30:
        conseil += "\n🏜️ Air très sec. Pensez à bien irriguer vos cultures."

    return conseil
def verifier_alertes_meteo(ville):
    meteo = get_meteo(ville)
    alertes = []

    if "erreur" in meteo:
        return alertes

    temp = meteo["temperature"]
    humidite = meteo["humidite"]
    vent = meteo["vent"]

    if temp > 30:  # ← abaissé de 38 à 30
        alertes.append({
            "type": "danger",
            "icone": "🔥",
            "message": f"Chaleur élevée à {ville} : {temp}°C ! Arrosez tôt le matin."
        })

    if humidite > 60:  # ← abaissé de 85 à 60
        alertes.append({
            "type": "warning",
            "icone": "🌧️",
            "message": f"Humidité élevée à {ville} : {humidite}%. Risque de maladies fongiques."
        })

    if humidite < 40:  # ← remonté de 20 à 40
        alertes.append({
            "type": "danger",
            "icone": "🏜️",
            "message": f"Air sec à {ville} : humidité {humidite}%. Pensez à irriguer."
        })

    if vent > 20:  # ← abaissé de 50 à 20
        alertes.append({
            "type": "warning",
            "icone": "💨",
            "message": f"Vents à {ville} : {vent} km/h. Surveillez vos cultures."
        })

    return alertes
def verifier_alertes_maladies(culture):
    culture = culture.lower()
    alertes = []

    maladies = {
        "maïs": {
            "icone": "🌽",
            "message": "⚠️ Saison à risque pour le maïs : surveillez les chenilles légionnaires et le charbon."
        },
        "sorgho": {
            "icone": "🌾",
            "message": "⚠️ Risque de mildiou sur le sorgho en période humide. Appliquez un fongicide."
        },
        "tomate": {
            "icone": "🍅",
            "message": "⚠️ Risque d'alternariose sur la tomate. Vérifiez les feuilles régulièrement."
        },
        "niébé": {
            "icone": "🫘",
            "message": "⚠️ Attention aux pucerons sur le niébé en saison sèche."
        },
        "arachide": {
            "icone": "🥜",
            "message": "⚠️ Risque de cercosporiose sur l'arachide. Rotation des cultures recommandée."
        }
    }

    for cle, info in maladies.items():
        if cle in culture:
            alertes.append({
                "type": "danger",
                "icone": info["icone"],
                "message": info["message"]
            })

    return alertes