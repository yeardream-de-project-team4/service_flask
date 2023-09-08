FROM python:3.9

RUN pip3 install --upgrade pip
RUN pip3 install flask Flask-Migrate gunicorn kafka-python
RUN pip3 install requests

RUN mkdir /opt/src
WORKDIR /opt/src

ADD src /opt/src

RUN chmod a+x init.sh

# Develop
CMD ["./init.sh"]

# Production
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "apps:create_app()"]