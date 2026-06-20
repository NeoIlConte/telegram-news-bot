from openai import OpenAI
import requests
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

chat_id = os.environ["TELEGRAM_CHAT_ID"]
token = os.environ["TELEGRAM_TOKEN"]
news_key = os.environ["NEWS_API_KEY"]

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": msg[:4000]
        }
    )

# NEWS INTERNAZIONALI
url = (
    f"https://newsapi.org/v2/top-headlines?"
    f"language=en&pageSize=10&apiKey={news_key}"
)

articles = requests.get(url).json()["articles"]

news_text = ""

for a in articles[:10]:
    news_text += f"""
Titolo: {a.get('title')}
Fonte: {a.get('source', {}).get('name')}
Descrizione: {a.get('description')}
"""

prompt1 = f"""
Agisci come il caporedattore di una testata economica internazionale.

Analizza queste notizie e seleziona le 5 più importanti.

Per ciascuna fornisci:
- titolo
- sintesi (3 righe)
- perché è importante

Notizie:

{news_text}
"""

r1 = client.responses.create(
    model="gpt-5-mini",
    input=prompt1
)

send("🌍 Rassegna Internazionale\n\n" + r1.output_text)

# TECH
prompt2 = """
Agisci come analista ICT.

Riporta le principali novità delle ultime 24 ore su:

- AI
- Cybersecurity
- Cloud
- Cisco
- Microsoft
- AWS
- Palo Alto
- CrowdStrike

Inoltre evidenzia eventuali notizie pubbliche relative a:
- VEM Sistemi
- Lutech
- Var Group
- Maticmind
- Engineering
- Almaviva

Formato executive per Account Manager.
"""

r2 = client.responses.create(
    model="gpt-5-mini",
    input=prompt2
)

send("🚀 Tech & System Integrator\n\n" + r2.output_text)
