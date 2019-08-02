#!/usr/bin/env python3
import os
import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup
import pysnooper

app = Flask(__name__)


@pysnooper.snoop()
def get_time():
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    response = requests.get("https://www.epochconverter.com/", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    time = soup.find_all("div", class_="inline")

    return time[0].getText()


@app.route("/")
def home():
    body = get_time()

    return Response(response=body, mimetype="text/html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host="0.0.0.0", port=port, debug=True)
