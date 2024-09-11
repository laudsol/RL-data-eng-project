import json
import redis
import time
import psutil
import os
from memory_profiler import memory_usage


data_base = 0  # 0 is nearly empty, 1 has 20M rows
use_case = 0
files = ['./data/test1.jsonl', './data/test2.jsonl', './data/test3.jsonl', './data/test4.jsonl']
file = files[use_case]

process = psutil.Process(os.getpid())

def memory_usage_in_mb():
    return process.memory_info().rss / 1024 / 1024

def get_seniority_value(key, redis_client):
    if redis_client.exists(key):
        seniority_value = redis_client.get(key).decode('utf-8')
    else:
        seniority_value = call_seniority_model(key)
        redis_client.set(key, seniority_value)

    return seniority_value


def call_seniority_model(key):
    time.sleep(1 / 1000)  # Simulate model processing time
    return 2  # Random value to simulate seniority


def script():
    redis_client = redis.Redis(host='localhost', port=6379, db=data_base)

    with open(file, 'r') as data_file:
        json_list = list(data_file)

        results = []
        for json_str in json_list:
            result = json.loads(json_str)
            seniority_key = result['company'] + result['title']
            seniority_value = get_seniority_value(seniority_key, redis_client)

            result['Seniority'] = seniority_value
            results.append(json.dumps(result))

        with open('./data/output1.jsonl', 'a') as write_file:
            write_file.write('\n'.join(results) + '\n')

initial_memory_usage = memory_usage_in_mb()

script()

final_memory_usage = memory_usage_in_mb()
total_memory_usage = final_memory_usage - initial_memory_usage

print(f"Memory Usage - psutil: {total_memory_usage:.6f} MB")

if __name__ == "__main__":
    mem_usage = memory_usage((script,))
    print(f"Memory usage - profiler: {mem_usage} MB")
