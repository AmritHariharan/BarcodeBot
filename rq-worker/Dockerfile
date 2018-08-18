FROM python:3.7

RUN pip install redis rq
ADD worker.py /app
WORKDIR /app

CMD ["python", "worker.py"]