import time
import requests
from datetime import datetime

from flask import jsonify
from bs4 import BeautifulSoup

from apps.crawler import blueprint
from apps.producer import MessageProducer


@blueprint.route("/")
def index():
    return "crawler index"


@blueprint.route("/test")
def route_test():
    return "crawler test"


@blueprint.route("/ticker/<ticker>", methods=["POST"])
def crawl(ticker):
    producer = MessageProducer()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }

    sleep_interval = 1

    # enter ticker news page
    url = f"https://finance.naver.com/item/news_news.naver?code={ticker}&page=1&sm=title_entity_id.basic&clusterId="
    time.sleep(sleep_interval)
    response = requests.get(url, headers)

    # parsing => delete related news on page 1
    soup = BeautifulSoup(response.text, "html.parser")
    all_tr = soup.select("table.type5 > tbody > tr:not(.relation_lst)")
    related_tr = soup.select(
        "table.type5 > tbody > tr.relation_lst > td > table > tbody > tr"
    )
    articles = list(set(all_tr) - set(related_tr))
    data = []

    # collect links and datetimes of articles on page 1
    for article in articles:
        # link
        link = article.select("a")[0].attrs["href"]
        # date
        date = article.select("td.date")[0].text.strip()
        date = datetime.strptime(date, "%Y.%m.%d %H:%M")
        data.append([date, f"https://finance.naver.com{link}"])

    # sort by datetime
    data.sort(reverse=True)

    # collect title and contents of articles
    for i in range(len(data)):
        # link
        url = data[i][1]

        # move to article page
        time.sleep(sleep_interval)
        response = requests.get(url, headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # title and content
        title = soup.select_one("strong.c")
        content = soup.select_one("div.scr01")
        if title and content:
            title = title.text.strip()
            content = content.text.strip()
            data[i].append(title)
            data[i].append(content)

    print("Crawling Success")
    print(f"Crawled {len(data)} articles for {ticker}")

    for date, link, title, content in data:
        msg = {
            "source": "crawled",
            "symbol": ticker,
            "link": link,
            "date": f"{date.year}{date.month:02}{date.day:02}",
            "title": title,
            "content": content,
        }
        producer.send_message("flask-postgres-csv", msg, auto_close=False)
        producer.send_message("flask-elk-csv", msg, auto_close=False)
    producer.close()
    return jsonify({"message": "Records have been uploaded to the database."})
