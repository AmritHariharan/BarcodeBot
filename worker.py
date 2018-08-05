from os import getenv
from redis import from_url
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = getenv('REDIS_URL', 'redis://localhost:6379')

conn = from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
