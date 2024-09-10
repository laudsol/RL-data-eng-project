import redis
import uuid

counter = 0
limit = 1000
redis_client = redis.Redis(host='localhost', port=6379, db=1)

while counter < limit:
    key = str(uuid.uuid4())
    redis_client.set(key, 2)
    counter += 1