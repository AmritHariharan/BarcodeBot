FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
    python-opencv \
    libsm6

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]