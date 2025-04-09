from flask import Flask
from threading import Thread
import requests
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot está rodando!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

def enviar_mensagem_discord():
    webhook_url = 'https://discord.com/api/webhooks/1359351359081681036/n7yVuIwZv4Hnrt3eUol18-x5i3ytid5Mjmhd4ajQK0GEvDvVPmTH5EwLOu_4rYaXjhjS'
    agora = datetime.datetime.utcnow()

    mensagem = {
        "content": f"🚨 TESTE de envio do webhook às {agora.strftime('%H:%M:%S')} UTC"
    }

    print(f"📤 Enviando mensagem para {webhook_url}")
    resposta = requests.post(webhook_url, json=mensagem)
    print(f"📝 Status code: {resposta.status_code}")
    print(f"📨 Resposta do Discord: {resposta.text}")

# Força o envio assim que iniciar
enviar_mensagem_discord()
