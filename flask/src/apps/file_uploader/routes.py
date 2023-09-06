import json, os, csv
from apps.file_uploader import blueprint
from apps.config import Config
from apps.producer import MessageProducer
from flask import request, render_template


@blueprint.route("/")
def index():
    return render_template("upload.html")


@blueprint.route("/test")
def route_test():
    return "file uploader test"


@blueprint.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    if file:
        reader = csv.reader(file.read().decode("utf-8").splitlines())
        next(reader, None)  # 헤더 건너뛰기

        brokers = Config.KAFKA_BROKERS
        topic = "topic-load-csv"
        producer = MessageProducer(brokers, topic)

        for source, symbol, link, date, title, content in reader:
            msg = {
                "source": source,
                "symbol": symbol,
                "link": link,
                "date": date,
                "title": title,
                "content": content,
            }
            producer.send_message(msg, auto_close=False)
        producer.close()
        return "Records have been uploaded to the database."

    return ":("
