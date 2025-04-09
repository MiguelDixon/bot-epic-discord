import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from keep_alive import manter_online

manter_online()


# Configurações do bot
TOKEN = 'SEU_TOKEN_AQUI'
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Rotas do Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está rodando!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# Iniciar o servidor web em uma thread separada
Thread(target=run_web).start()

# Eventos e comandos do bot
@bot.event
async def on_ready():
    print(f'Logado como {bot.user}')

# Outros comandos e eventos aqui
if datetime.datetime.today().weekday() == 3:  # Quinta-feira (3)
if True:  # Força a execução sempre que rodar

# Iniciar o bot
bot.run(TOKEN)
