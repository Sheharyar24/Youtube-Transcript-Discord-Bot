from flask import Flask
from threading import Thread

# This file is used to run the bot on a web server
app = Flask('')
@app.route('/')
def home():
    return "Discord Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
