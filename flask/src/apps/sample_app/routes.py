import json
from apps.sample_app import blueprint
from apps.config import Config
from apps.producer import MessageProducer
from flask import request


@blueprint.route("/")
def route_default():
    return "sample_app index"


@blueprint.route("/test")
def route_test():
    return "sample_app test22"


@blueprint.route("/say/<word>")
def route_say(word):
    return word


@blueprint.route("/send", methods=["POST"])
def upload():
    data = request.get_json()
    name = data["name"]
    age = data["age"]
    return json.dumps({name: name, age: age}), 200


@blueprint.route("/do", methods=["POST"])
def do():
    brokers = Config.KAFKA_BROKERS
    topic = "test-postgres-topic"
    producer = MessageProducer(brokers, topic)

    # do something

    data = {"name": "mark", "age": 25}
    result = producer.send_message(data)
    return result, 200
