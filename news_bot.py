from openai import OpenAI
import requests
import os
from datetime import datetime

# =========================
# CONFIG
# =========================

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

chat_id = os.environ["TELEGRAM_CHAT_ID"]
telegram_token = os.environ["TELEGRAM_TOKEN"]
news_key = os.environ["NEWS_API_KEY"]

MAX_TELEGRAM_LENGTH = 3900

# =========================
# TELEGRAM
# =========================

def send(msg):
    if not msg:
        return

    if len(msg) > MAX_TELEGRAM_LENGTH:
        msg = msg[:MAX_TELEGRAM_LENGTH] + "\n\n...[troncato]"

    requests.post(
        f"https://api.telegram.org/bot{telegram_token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": msg
        },
        timeout=30
    )

# =========================
# NEWS API
# =========================

def get_news(url):
    try:
        response = requests.get(url, timeout=30)
        data = response.json()

        if data.get("status") != "ok":
            return []

        return data.get("articles", [])

    except Exception as e:
        print(f"Errore NewsAPI: {e}")
        return []

# =========================
# GPT
# =========================

def ask_gpt(prompt):

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text

# =========================
# HEADER
# =========================

today = datetime.now().strftime("%d/%m/%Y")

# ==================================================
# 1. RASSEGNA INTERNAZIONALE
# ==================================================

world_url = (
    "https://newsapi.org/v2/top-headlines?"
    f"language=en&pageSize=20&apiKey={news_key}"
)

world_articles = get_news(world_url)

world_text = ""

for a in world_articles[:15]:

    title = a.get("title", "")
    source = a.get("source", {}).get("name", "")
    desc = a.get("description", "")

    world_text += f"""
Titolo: {title}
Fonte: {source}
Descrizione: {desc}

"""

prompt_world = f"""
Agisci come caporedattore internazionale.

Data: {today}

Analizza le notizie seguenti.

Seleziona le 5 più importanti.

Per ciascuna indica:

- Titolo
- Sintesi (massimo 3 righe)
- Perché è importante

Concludi con:

"Implicazioni per Europa e Italia"

NOTIZIE:

{world_text}
"""

world_report = ask_gpt(prompt_world)

send(
    f"🌍 RASSEGNA INTERNAZIONALE - {today}\n\n"
    f"{world_report}"
)

# ==================================================
# 2. TECH & CYBER
# ==================================================

tech_url = (
    "https://newsapi.org/v2/everything?"
    "q=(AI OR cybersecurity OR cloud OR Cisco OR Microsoft "
    "OR AWS OR Palo Alto OR CrowdStrike OR Google Cloud)"
    "&language=en"
    "&sortBy=publishedAt"
    "&pageSize=30"
    f"&apiKey={news_key}"
)

tech_articles = get_news(tech_url)

tech_text = ""

for a in tech_articles[:20]:

    title = a.get("title", "")
    source = a.get("source", {}).get("name", "")
    desc = a.get("description", "")

    tech_text += f"""
Titolo: {title}
Fonte: {source}
Descrizione: {desc}

"""

prompt_tech = f"""
Agisci come ICT Strategy Advisor.

Pubblico:
Account Manager VEM Sistemi.

Analizza le notizie.

Produci:

🚀 TOP NEWS TECH

Per ogni news:
- titolo
- sintesi
- impatto per CIO/CISO

🛡 CYBER ALERT

Evidenzia:
- vulnerabilità
- incidenti
- ransomware
- nuove minacce

☁ CLOUD & AI

Riassumi trend rilevanti.

📌 OPPORTUNITÀ COMMERCIALI

Indica:
- opportunità VEM
- possibili follow-up commerciali

NOTIZIE:

{tech_text}
"""

tech_report = ask_gpt(prompt_tech)

send(
    f"🚀 TECH & CYBER - {today}\n\n"
    f"{tech_report}"
)

# ==================================================
# 3. ACCOUNT INTELLIGENCE
# ==================================================

account_prompt = f"""
Agisci come Account Intelligence Analyst.

Data: {today}

Prepara un briefing executive.

Concentrati su:

CLIENTI E TARGET:
- Mediobanca
- Tesya
- Alayan

SYSTEM INTEGRATOR:
- VEM Sistemi
- Lutech
- Var Group
- Maticmind
- Engineering
- Almaviva

Per ciascuna organizzazione evidenzia SOLO se rilevante:

- acquisizioni
- partnership
- investimenti
- cybersecurity
- cloud
- AI
- data center
- nomine CIO/CISO
- trasformazione digitale

Se non emergono elementi significativi,
scrivi "Nessuna evidenza rilevante".

Concludi con:

🎯 PRIORITÀ COMMERCIALI DEL GIORNO

(max 5 punti)
"""

account_report = ask_gpt(account_prompt)

send(
    f"📈 ACCOUNT INTELLIGENCE - {today}\n\n"
    f"{account_report}"
)

print("Messaggi inviati correttamente.")
