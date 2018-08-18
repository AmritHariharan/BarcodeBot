FROM ubuntu:18.04

RUN apt update && apt install python3.7 && pip3 install pipenv

COPY ../docker /app
WORKDIR /app

RUN pipenv install --system

EXPOSE 8080

CMD ["python3", "app.py"]