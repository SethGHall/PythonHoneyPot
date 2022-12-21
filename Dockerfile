FROM python:3.9

ADD HoneyPotWebserver.py HoneyPotWebserver.py
ADD config.ini config.ini

EXPOSE 8080

CMD ["python", "./HoneyPotWebserver.py"]

