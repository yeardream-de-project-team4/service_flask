import json
from apps.keum_coin_app import blueprint
from apps.config import Config
from apps.producer import MessageProducer
from flask import request


@blueprint.route("/")
def route_default():
    return "coin_app index"


@blueprint.route("/test")
def route_test():
    return "coin_app test22"


@blueprint.route("/say/<word>")
def route_say(word):
    return word


@blueprint.route("/send", methods=["POST"])
def upload():
    data = request.get_json()
    name = data["name"]
    price = data["price"]
    return json.dumps({name: name, price: price}), 200


@blueprint.route("/do", methods=["POST"])
def do():
    brokers = Config.KAFKA_BROKERS
    topic = "keum-coin-postgres-topic"
    producer = MessageProducer(brokers, topic)

    # do something

    data = {"name": "KRW-BTC", "price": 1000}
    result = producer.send_message(data)
    return result, 200