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
    agora = datetime.datetime.now(datetime.timezone.utc)

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
                    desconto = oferta.get('discountSetting', {}).get('discountPercentage', 0)
                    if desconto == 0:
                        continue  # não é grátis

                    titulo = jogo['title']
                    imagem = jogo['keyImages'][0]['url']
                    try:
                        slug = jogo['catalogNs']['mappings'][0]['pageSlug']
                        link = f"https://store.epicgames.com/pt-BR/p/{slug}"
                    except:
                        link = "https://store.epicgames.com/pt-BR/free-games"

                    return titulo, link, imagem
    return None, None, None

def enviar_mensagem_discord():
    webhook_url = 'https://discord.com/api/webhooks/1359351359081681036/n7yVuIwZv4Hnrt3eUol18-x5i3ytid5Mjmhd4ajQK0GEvDvVPmTH5EwLOu_4rYaXjhjS'
    titulo, link, imagem = buscar_jogo_gratis_epic()

    if titulo and link and imagem:
        embed = {
            "title": f"🎮 {titulo}",
            "description": f"🆓 Jogo grátis da semana na Epic Games!\n🔗 [Resgatar agora]({link})",
            "image": {"url": imagem},
            "color": 16753920  # Amarelinho bonito
        }
        payload = {
            "content": "🎁 Novo jogo grátis disponível!",
            "embeds": [embed]
        }
    else:
        payload = {
            "content": "❗ Não consegui buscar o jogo grátis dessa semana. Verifica manualmente: https://store.epicgames.com/pt-BR/free-games"
        }

    r = requests.post(webhook_url, json=payload)
    print("✅ Mensagem enviada pro Discord! Status:", r.status_code)

hoje = datetime.datetime.today().weekday()
if True:
    enviar_mensagem_discord()
