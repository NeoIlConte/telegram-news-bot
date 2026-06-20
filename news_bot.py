from openai import OpenAI
import requests
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

chat_id = os.environ["TELEGRAM_CHAT_ID"]
token = os.environ["TELEGRAM_TOKEN"]

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": msg
        }
    )

prompt1 = """
Prepara una rassegna stampa internazionale.
Seleziona le 5 notizie più importanti del giorno da fonti autorevoli.
Sintesi professionale in italiano.
"""

r1 = client.responses.create(
    model="gpt-5",
    input=prompt1
)

send("🌍 Rassegna Internazionale\n\n" + r1.output_text)

prompt2 = """
Prepara una rassegna Tech e System Integrator italiani.

Includi:
- AI
- Cybersecurity
- Cloud
- Cisco
- Microsoft
- Palo Alto
- CrowdStrike
- AWS

Analizza anche:
VEM Sistemi
Lutech
Var Group
Maticmind
Engineering
Almaviva

Sintesi executive.
"""

r2 = client.responses.create(
    model="gpt-5",
    input=prompt2
)

send("🚀 Tech & System Integrator\n\n" + r2.output_text)
