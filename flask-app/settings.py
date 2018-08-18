import os

STATIC_IMAGES_DIR = 'static/images/examples'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'mp3'}

REDIS_HOST = os.environ['REDIS_MASTER_SERVICE_HOST'] \
    if os.environ.get('GET_HOSTS_FROM', '') == 'env' else 'redis-master'
REDIS_PORT = 6379