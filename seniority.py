import json
import redis
import psutil
import os
import time

data_base = 1 # 0 can be emptied, 1 has 20M rows
use_case = 2
files = ['./data/test1.jsonl', './data/test2.jsonl', './data/test3.jsonl']
file = files[use_case]

def get_seniority_value(key, redis):
    redis_read = 0
    redis_write = 0
    start_time = time.perf_counter()
    write_counter = 0
    if redis.exists(key):
        seniority_value = redis.get(key).decode('utf-8')
        end_time = time.perf_counter()
        redis_read += end_time - start_time
    else:
        # seniority_start = time.perf_counter()
        seniority_value = call_seniority_model(key)
        # seniority_end = time.perf_counter()
        seniority_time = 1/1000

        redis.set(key, seniority_value)
        end_time = time.perf_counter()
        redis_write += end_time - start_time - seniority_time

        write_counter = 1
    return [seniority_value, redis_read, redis_write, write_counter]


def call_seniority_model(key):
    # think about writing an algo to slow the function when it gets more hits
    time.sleep(1 / 1000)
    return 2 # return random 1 - 7, lower is more frequent 

def script():
    total_redis_read = 0
    total_redis_write = 0
    write_counter = 0

    redis_client = redis.Redis(host='localhost', port=6379, db=data_base)
    with open(file, 'r') as data_file:
        json_list = list(data_file)

        results = []
        for json_str in json_list:
            result = json.loads(json_str)
            seniority_key = result['company'] + result['title']
            seniority_value = get_seniority_value(seniority_key, redis_client)
            result['Seniority'] = seniority_value[0]
            total_redis_read += seniority_value[1]
            total_redis_write += seniority_value[2]
            write_counter += seniority_value[3]
            results.append(json.dumps(result))

        with open('./data/output1.jsonl', 'a') as write_file:
                write_file.write('\n'.join(results) + '\n')
    
    print(f"Redis read {total_redis_read}")
    print(f"Redis write {total_redis_write}")
    print(f"Total Redis writes {write_counter}")

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