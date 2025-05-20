from flask import Flask
from threading import Thread
import requests
from datetime import datetime, timezone
import schedule
import time
import pytz

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está rodando!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

def buscar_jogos_gratis_semana():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=pt-BR&country=BR"
    response = requests.get(url)
    dados = response.json()

    agora = datetime.utcnow().replace(tzinfo=timezone.utc)
    jogos = dados['data']['Catalog']['searchStore']['elements']

    jogos_gratis = []

    for jogo in jogos:
        promocoes = jogo.get('promotions')
        if not promocoes:
            continue

        ofertas_ativas = promocoes.get('promotionalOffers')
        if not ofertas_ativas or not ofertas_ativas[0]['promotionalOffers']:
            continue

        for oferta in ofertas_ativas[0]['promotionalOffers']:
            inicio = datetime.fromisoformat(oferta['startDate'].replace('Z', '+00:00'))
            fim = datetime.fromisoformat(oferta['endDate'].replace('Z', '+00:00'))

            if inicio <= agora <= fim:
                titulo = jogo['title']
                try:
                    slug = jogo['catalogNs']['mappings'][0]['pageSlug']
                    link = f"https://store.epicgames.com/pt-BR/p/{slug}"
                except:
                    link = "https://store.epicgames.com/pt-BR/free-games"

                capa = None
                for img in jogo['keyImages']:
                    if img['type'] in ['DieselStoreFrontWide', 'OfferImageWide', 'OfferImageTall']:
                        capa = img['url']
                        break

                jogos_gratis.append({
                    'titulo': titulo,
                    'link': link,
                    'imagem': capa or "https://cdn2.unrealengine.com/egs-freegames-weekly-1920x1080-1920x1080-02abc25b0b96.jpg"
                })

    return jogos_gratis

def enviar_mensagem_discord():
    webhook_url = 'https://discord.com/api/webhooks/1359351359081681036/n7yVuIwZv4Hnrt3eUol18-x5i3ytid5Mjmhd4ajQK0GEvDvVPmTH5EwLOu_4rYaXjhjS'
    jogos = buscar_jogos_gratis_semana()

    if jogos:
        for jogo in jogos:
            mensagem = {
                "content": "@everyone",
                "embeds": [
                    {
                        "title": f"🎮 Jogo grátis da semana: {jogo['titulo']}",
                        "description": f"🔗 [Resgatar agora]({jogo['link']})",
                        "image": {
                            "url": jogo['imagem']
                        },
                        "color": 0x00ff00
                    }
                ]
            }
            r = requests.post(webhook_url, json=mensagem)
            print(f"✅ Mensagem enviada: {jogo['titulo']} | Status: {r.status_code}")
    else:
        mensagem = {
            "content": "@everyone ❗ Nenhum jogo grátis encontrado no momento. Verifica manualmente: https://store.epicgames.com/pt-BR/free-games"
        }
        r = requests.post(webhook_url, json=mensagem)
        print("⚠️ Nenhum jogo encontrado. Status:", r.status_code)

# Ajuste para usar o fuso horário de Brasília
brasil_tz = pytz.timezone('America/Sao_Paulo')
schedule.every().friday.at("13:00").do(enviar_mensagem_discord)

# Loop contínuo
while True:
    schedule.run_pending()
    time.sleep(1)

