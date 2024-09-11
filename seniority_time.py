import json
import redis
import time

data_base = 0  # 0 is nearly empty, 1 has 20M rows
use_case = 3
files = ['./data/test1.jsonl', './data/test2.jsonl', './data/test3.jsonl', './data/test4.jsonl']
file = files[use_case]

def get_seniority_value(key, redis_client):
    redis_read_time = 0
    redis_write_time = 0
    write_counter = 0

    start_time = time.perf_counter()
    if redis_client.exists(key):
        seniority_value = redis_client.get(key).decode('utf-8')
        redis_read_time += time.perf_counter() - start_time
    else:
        seniority_value = call_seniority_model(key)

        redis_write_start = time.perf_counter()
        redis_client.set(key, seniority_value)
        redis_write_time += time.perf_counter() - redis_write_start

        write_counter = 1

    return seniority_value, redis_read_time, redis_write_time, write_counter


def call_seniority_model(key):
    time.sleep(1 / 1000)  # Simulate model processing time
    return 2  # Hardcoded value...would be dynamic in real life


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
            seniority_value, redis_read, redis_write, write_count = get_seniority_value(seniority_key, redis_client)

            result['Seniority'] = seniority_value
            total_redis_read += redis_read
            total_redis_write += redis_write
            write_counter += write_count
            results.append(json.dumps(result))

        with open('./data/output1.jsonl', 'a') as write_file:
            write_file.write('\n'.join(results) + '\n')

    print(f"Total Redis Read Time: {total_redis_read:.6f} seconds")
    print(f"Total Redis Write Time: {total_redis_write:.6f} seconds")
    print(f"Total Redis Write Operations: {write_counter}")

start_time = time.perf_counter()
script()
end_time = time.perf_counter()

execution_time = end_time - start_time
print(f"Execution Time: {execution_time:.6f} seconds")
