import json
import redis
import psutil
import os
import time

file = './data/test1.jsonl'

def get_seniority_value(key, redis):
    redis_read = 0
    redis_write = 0
    start_time = time.perf_counter()
    if redis.exists(key):
        seniority_value = redis.get(key).decode('utf-8')
        end_time = time.perf_counter()
        redis_read += end_time - start_time
    else:
        seniority_value = call_seniority_model(key)
        redis.set(key, seniority_value)
        end_time = time.perf_counter()
        redis_write += end_time - start_time
    return [seniority_value, redis_read, redis_write]


def call_seniority_model(key):
    # think about writing an algo to slow the function when it gets more hits
    time.sleep(1 / 1000)
    return 2 # return random 1 - 7, lower is more frequent 

def script():
    total_redis_read = 0
    total_redis_write = 0

    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    with open(file, 'r') as data_file:
        json_list = list(data_file)

    for json_str in json_list:
        result = json.loads(json_str)
        seniority_key = result['company'] + result['title']
        seniority_value = get_seniority_value(seniority_key, redis_client)
        result['Seniority'] = seniority_value[0]
        total_redis_read += seniority_value[1]
        total_redis_write += seniority_value[2]

        with open('./data/output1.jsonl', 'a') as write_file:
            write_file.write(json.dumps(result) + '\n')
    
    print(f"Redis read {total_redis_read}")
    print(f"Redis write {total_redis_write}")

    pass

start_time = time.perf_counter()
script()
end_time = time.perf_counter()

execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")

# TO DO: Lazy Loading: Instead of reading the entire file into a list at once, you could iterate over the file line by line to reduce the memory spike caused by loading the file content into memory.
# with open('./data/test2.jsonl', 'r') as data_file:
#     for json_str in data_file:
#         result = json.loads(json_str)
# Process each JSON object