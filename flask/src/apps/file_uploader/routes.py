import csv
from apps.file_uploader import blueprint
from apps.config import Config
from apps.producer import MessageProducer
from flask import request, render_template, jsonify
from minio import Minio


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

        producer = MessageProducer()

        for source, symbol, link, date, title, content in reader:
            msg = {
                "source": source,
                "symbol": symbol,
                "link": link,
                "date": date,
                "title": title,
                "content": content,
            }
            producer.send_message("flask-postgres-csv", msg, auto_close=False)
            producer.send_message("flask-elk-csv", msg, auto_close=False)
        producer.close()
        return jsonify(
            {"message": "Records have been uploaded to the database."}
        )
    return jsonify({"message": "Failed to upload file"})


@blueprint.route("/big_upload", methods=["POST"])
def upload_big_file():
    uploaded_file = request.files["big_file"]
    if uploaded_file.filename != "":
        client = Minio(
            Config.MINIO_HOST,
            Config.MINIO_USER,
            Config.MINIO_PASSWORD,
            secure=False,
        )
        client.put_object(
            "hadoop-bucket",
            uploaded_file.filename,
            uploaded_file,
            length=-1,
            part_size=10 * 1024 * 1024,
        )

        producer = MessageProducer()
        msg = {"bucket": "hadoop-bucket", "filename": uploaded_file.filename}
        producer.send_message("flask-hadoop-file", msg, auto_close=False)
        producer.send_message("flask-elk-file", msg, auto_close=False)
        producer.close()
        return jsonify({"message": "File uploaded to MinIO successfully!"})

    return jsonify({"message": "Failed to upload file"})
