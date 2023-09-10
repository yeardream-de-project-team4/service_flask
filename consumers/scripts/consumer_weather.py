import requests


def callback_weather(message):
    num = message.value["num"]  # {'num': '20'}
    requests.post(f"http://haproxy:80/taehoon/do/{num}")
