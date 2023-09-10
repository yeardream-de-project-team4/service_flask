import requests


def callback_market(message):
    num = message.value["num"]
    requests.post(f"http://haproxy:80/market/trade/{num}")
