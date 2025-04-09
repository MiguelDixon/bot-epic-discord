from flask import Flask
from threading import Thread
import requests
import datetime

# ======== KEEP ALIVE (Render) ========
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está rodando!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

# ======== FUNÇÃO PARA PEGAR O JOGO GRÁTIS DA EPIC ========
def buscar_jogo_gratis_epic():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=pt-BR"
    response = requests.get(url)
    dados = response.json()

    try:
        jogos = dados['data']['Catalog']['searchStore']['elements']
        for jogo in jogos:
            if jogo.get('promotions') and jogo['promotions'].get('promotionalOffers'):
                titulo = jogo['title']
                slug = jogo['productSlug']
                link = f"https://store.epicgames.com/pt-BR/p/{slug}"
                return titulo, link
    except:
        return None, None

# ======== ENVIAR MENSAGEM PRO WEBHOOK ========
def enviar_mensagem_discord():
    webhook_url = 'COLE_SEU_WEBHOOK_AQUI'
    titulo, link = buscar_jogo_gratis_epic()

    if titulo and link:
        mensagem = {
            "content": f"🎮 **Jogo grátis da semana na Epic!**\n🕹️ {titulo}\n🔗 {link}"
        }
    else:
        mensagem = {
            "content": "❗ Não consegui buscar o jogo grátis dessa semana. Verifica manualmente: https://store.epicgames.com/pt-BR/free-games"
        }

    requests.post(webhook_url, json=mensagem)
    print("Mensagem enviada!")

# ======== VERIFICAR SE É QUINTA-FEIRA ========
hoje = datetime.datetime.today().weekday()
if true:  # 3 = quinta-feira
    enviar_mensagem_discord()
