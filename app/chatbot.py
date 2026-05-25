import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import spacy
from app.meteo import conseil_meteo
from app.database import get_db
from app.regions import REGIONS

nlp = spacy.load("fr_core_news_sm")

INTENTIONS = {
    "meteo": ["météo", "temps", "pluie", "soleil", "température", "climat", "vent"],
    "plantation": ["planter", "plantation", "semer", "semis", "période", "quand"],
    "maladie": ["maladie", "parasite", "insecte", "champignon", "traitement", "symptôme"],
    "recolte": ["récolte", "récolter", "cueillir", "moissonner"],
    "sol": ["sol", "terre", "fertilité", "engrais", "fumure"],
    "salutation": ["bonjour", "bonsoir", "salut", "hello"],
    "region": ["région", "zone", "sahel", "est", "nord", "centre", "hauts-bassins", "gaoua", "bobo", "ouahigouya", "dori", "fada"],
}

def detecter_intention(texte):
    texte_lower = texte.lower()
    for region in REGIONS.keys():
        if region.lower() in texte_lower or texte == region:
            return "region"
    for intention, mots_cles in INTENTIONS.items():
        for mot in mots_cles:
            if mot.lower() in texte_lower:
                return intention
    return "inconnu"

def extraire_ville(texte):
    doc = nlp(texte)
    for ent in doc.ents:
        if ent.label_ in ["LOC", "GPE"]:
            return ent.text
    mots = texte.split()
    for i, mot in enumerate(mots):
        if mot.lower() in ["à", "a", "pour", "de", "en"] and i + 1 < len(mots):
            return mots[i + 1]
    return "Ouagadougou"

def repondre_plantation():
    return """🌱 Conseils de plantation au Burkina Faso :

📅 Saison des pluies (Mai - Octobre) :
- Maïs : Planter en Mai-Juin
- Mil/Sorgho : Planter en Juin-Juillet
- Niébé : Planter en Juillet-Août

☀️ Saison sèche (Novembre - Avril) :
- Maraîchage : Tomates, oignons, choux
- Irrigation obligatoire

💡 Conseil : Attendez les premières pluies pour semer les céréales."""

def repondre_maladie():
    return """🦠 Maladies courantes et traitements :

🌽 Maïs :
- Charbon du maïs → Utiliser des semences certifiées
- Chenilles légionnaires → Traitement au neem

🌾 Mil/Sorgho :
- Mildiou → Fongicide recommandé
- Criquet → Alerte précoce, traitement collectif

🍅 Tomate :
- Alternariose → Bouillie bordelaise
- Mouche blanche → Insecticide bio"""

def repondre_sol():
    return """🌍 Gestion du sol :

✅ Bons types de sol :
- Sol argileux → Sorgho, coton
- Sol sableux → Arachide, niébé
- Sol limoneux → Maïs, légumes

💧 Amélioration :
- Compost maison
- Rotation des cultures
- Zaï pour zones dégradées
- Cordons pierreux contre l'érosion"""

def repondre_recolte():
    return """🌾 Conseils de récolte :

📅 Périodes :
- Maïs : Septembre - Octobre
- Mil : Octobre - Novembre
- Sorgho : Octobre - Décembre
- Niébé : Septembre - Octobre

📦 Conservation :
- Greniers bien ventilés
- Sacs hermétiques
- Traitement au phosphure"""

def repondre_region(region_nom):
    region_data = None
    for cle, data in REGIONS.items():
        if cle.lower() == region_nom.lower() or cle == region_nom:
            region_data = data
            region_nom = cle
            break
    if not region_data:
        regions_list = "\n".join([f"• {r}" for r in REGIONS.keys()])
        return f"❌ Région non reconnue.\n\nRégions disponibles :\n{regions_list}"
    r = region_data
    cultures = ", ".join(r["cultures"])
    plantations = "\n".join([f"  • {c} : {p}" for c, p in r["plantation"].items()])
    return f"""🌍 Région : {region_nom}
🌦️ Ville météo : {r['ville_meteo']}
🌱 Cultures principales : {cultures}

🌍 Sol : {r['sol']}
💡 Conseil sol : {r['conseils_sol']}

📅 Périodes de plantation :
{plantations}

ℹ️ Particularités : {r['particularites']}"""

def sauvegarder_conversation(question, reponse):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (question, reponse) VALUES (?, ?)", (question, reponse))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")

def chatbot_repondre(question):
    intention = detecter_intention(question)
    if intention == "salutation":
        reponse = "👋 Bonjour ! Je suis votre assistant agricole. Comment puis-je vous aider ?"
    elif intention == "meteo":
        ville = extraire_ville(question)
        reponse = conseil_meteo(ville)
    elif intention == "plantation":
        reponse = repondre_plantation()
    elif intention == "maladie":
        reponse = repondre_maladie()
    elif intention == "sol":
        reponse = repondre_sol()
    elif intention == "recolte":
        reponse = repondre_recolte()
    elif intention == "region":
        reponse = repondre_region(question)
    else:
        reponse = """🤔 Je n'ai pas bien compris.

Posez-moi des questions sur :
- 🌤️ La météo
- 🌱 La plantation
- 🦠 Les maladies
- 🌍 Le sol
- 🌾 La récolte
- 🗺️ Votre région"""
    sauvegarder_conversation(question, reponse)
    return reponse
