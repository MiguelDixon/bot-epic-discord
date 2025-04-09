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

def buscar_jogos_gratis_semana():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=pt-BR&country=BR"
    response = requests.get(url)
    dados = response.json()

    jogos = dados['data']['Catalog']['searchStore']['elements']
    agora = datetime.datetime.now(datetime.timezone.utc)

    jogos_gratis = []

    for jogo in jogos:
        promocoes = jogo.get('promotions')
        if not promocoes:
            continue

        todas_ofertas = []
        if promocoes.get('promotionalOffers'):
            todas_ofertas += promocoes['promotionalOffers']
        if promocoes.get('upcomingPromotionalOffers'):
            todas_ofertas += promocoes['upcomingPromotionalOffers']

        for grupo in todas_ofertas:
            for oferta in grupo.get('promotionalOffers', []):
                inicio = datetime.datetime.fromisoformat(oferta['startDate'].replace('Z', '+00:00'))
                fim = datetime.datetime.fromisoformat(oferta['endDate'].replace('Z', '+00:00'))

                if inicio <= agora <= fim:
                    desconto = oferta.get('discountSetting', {}).get('discountPercentage', 0)
                    if desconto == 100:
                        titulo = jogo['title']
                        imagem = jogo['keyImages'][0]['url']
                        try:
                            slug = jogo['catalogNs']['mappings'][0]['pageSlug']
                            link = f"https://store.epicgames.com/pt-BR/p/{slug}"
                        except:
                            link = "https://store.epicgames.com/pt-BR/free-games"
                        jogos_gratis.append((titulo, link, imagem))

    return jogos_gratis
def enviar_mensagem_discord():
    webhook_url = 'https://discord.com/api/webhooks/1359351359081681036/n7yVuIwZv4Hnrt3eUol18-x5i3ytid5Mjmhd4ajQK0GEvDvVPmTH5EwLOu_4rYaXjhjS'
    jogos = buscar_jogos_gratis_semana()

    if jogos:
        embeds = []
        for titulo, link, imagem in jogos:
            embeds.append({
                "title": f"🎮 {titulo}",
                "description": f"🆓 Grátis agora na Epic Games!\n🔗 [Resgatar aqui]({link})",
                "image": {"url": imagem},
                "color": 16753920
            })

        payload = {
            "content": f"🎁 Jogos grátis disponíveis na Epic essa semana ({len(jogos)}):",
            "embeds": embeds
        }
    else:
        payload = {
            "content": "❗ Nenhum jogo grátis encontrado no momento. Verifica manualmente: https://store.epicgames.com/pt-BR/free-games"
        }

    r = requests.post(webhook_url, json=payload)
    print("✅ Mensagem enviada pro Discord! Status:", r.status_code)

hoje = datetime.datetime.today().weekday()
if True:
    enviar_mensagem_discord()
