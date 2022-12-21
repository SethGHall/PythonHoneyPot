# PythonHoneyPot
A Simple Python HoneyPot web server which intercepts GET requests and displays a text stream of messages using chunked transfer encoding

#Todo:
Containerize with Docker

build docker container - from root of PythonHoneyPot Project

docker build -t python-honeypot .

had this issue https://runnable.com/docker/binding-docker-ports set HOSTNAME = 0.0.0.0

docker run -it -p 8080:8080 python-honeypot 