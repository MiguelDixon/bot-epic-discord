from flask import Flask
from threading import Thread
import requests
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está rodando!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

def buscar_jogo_gratis_epic():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=pt-BR&country=BR"
    response = requests.get(url)
    dados = response.json()

    jogos = dados['data']['Catalog']['searchStore']['elements']
    agora = datetime.datetime.utcnow()

    for jogo in jogos:
        promocoes = jogo.get('promotions')
        if not promocoes:
            continue

        ofertas_ativas = promocoes.get('promotionalOffers')
        if ofertas_ativas:
            for oferta in ofertas_ativas[0]['promotionalOffers']:
                inicio = datetime.datetime.fromisoformat(oferta['startDate'].replace('Z', '+00:00'))
                fim = datetime.datetime.fromisoformat(oferta['endDate'].replace('Z', '+00:00'))

                if inicio <= agora <= fim:
                    titulo = jogo['title']
                    try:
                        slug = jogo['catalogNs']['mappings'][0]['pageSlug']
                        link = f"https://store.epicgames.com/pt-BR/p/{slug}"
                    except:
                        link = "https://store.epicgames.com/pt-BR/free-games"
                    return titulo, link
    return None, None

def enviar_mensagem_discord():
    webhook_url = 'https://discord.com/api/webhooks/1359351359081681036/n7yVuIwZv4Hnrt3eUol18-x5i3ytid5Mjmhd4ajQK0GEvDvVPmTH5EwLOu_4rYaXjhjS'
    titulo, link = buscar_jogo_gratis_epic()
    print("Tentando enviar mensagem para o webhook:", webhook_url)
    print("Mensagem:", mensagem)

    if titulo and link:
        mensagem = {
            "content": f"🎮 **Jogo grátis da semana na Epic Games!**\n🕹️ {titulo}\n🔗 {link}"
        }
    else:
        mensagem = {
            "content": "❗ Não consegui buscar o jogo grátis dessa semana. Verifica manualmente: https://store.epicgames.com/pt-BR/free-games"
        }

    requests.post(webhook_url, json=mensagem)
    print("✅ Mensagem enviada pro Discord!")

hoje = datetime.datetime.today().weekday()
if True:
    enviar_mensagem_discord()
