from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Estou vivo!"

def manter_online():
    t = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080})
    t.start()
