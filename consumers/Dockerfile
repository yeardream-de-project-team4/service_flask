FROM python:3.9

RUN pip3 install --upgrade pip
RUN pip3 install kafka-python requests

# 3rd party library
# RUN pip3 install [library]

ADD ./scripts /scripts
RUN chmod -R a+x /scripts

CMD ["python3", "/scripts/consumer.py"]