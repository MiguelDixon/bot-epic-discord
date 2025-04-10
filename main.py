from flask import Flask
from threading import Thread
import requests
from datetime import datetime, timezone
import schedule
import time

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

                capa = ""
                tipos_preferidos = ["DieselStoreFrontWide", "DieselGameBox", "OfferImageWide"]

                for tipo in tipos_preferidos:
                    for img in jogo['keyImages']:
                        if img['type'] == tipo:
                            capa = img['url']
                            break
                    if capa:
                        break

                jogos_gratis.append({
                    'titulo': titulo,
                    'link': link,
                    'imagem': capa
                })

    return jogos_gratis

def enviar_mensagem_discord():
    webhook_url = 'https://discord.com/api/webhooks/1359351359081681036/n7yVuIwZv4Hnrt3eUol18-x5i3ytid5Mjmhd4ajQK0GEvDvVPmTH5EwLOu_4rYaXjhjS'
    jogos = buscar_jogos_gratis_semana()

    if jogos:
        for jogo in jogos:
            embed = {
                "title": f"🎮 Jogo grátis da semana: {jogo['titulo']}",
                "description": f"🔗 [Resgatar agora]({jogo['link']})",
                "color": 0x00ff00
            }

            if jogo['imagem']:
                embed["image"] = {"
