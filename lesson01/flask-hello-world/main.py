import os

from flask import Flask
app = Flask(__name__)

@app.route('hello/<name>/')
def hello_name(name):
    return 'Hello, {}!'.format(name)

@app.route('hola/<name>/')
def hola_name(name):
    return 'Hola, {}!'.format(name)

@app.route('/')
def hello_world():
    return 'Hello, world!'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8523))
    app.run(host='0.0.0.0', port=port)

