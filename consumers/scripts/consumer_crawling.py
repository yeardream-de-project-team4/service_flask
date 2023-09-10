import requests


def callback_crawling(message):
    ticker = message.value["ticker"]
    requests.post(f"http://haproxy:80/crawl/ticker/{ticker}")
