import json
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

with open('./data/test1.jsonl', 'r') as json_file:
    json_list = list(json_file)

def check_and_cache_data(key):
    # Check if the key exists in the cache
    if redis_client.exists(key):
        # If the key exists, print the cached value
        cached_value = redis_client.get(key).decode('utf-8')
        print(f"Cache hit: {cached_value}")
    else:
        # If the key doesn't exist, write it to the cache
        value = get_seniority_value
        redis_client.set(key, value)
        print(f"Cache miss: Writing '{value}' to cache with key '{key}'")

def get_seniority_value(key):
    return 2

for json_str in json_list:
    result = json.loads(json_str)
    key = result['company'] + result['title']
    check_and_cache_data(key)

