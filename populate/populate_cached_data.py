import json
import uuid
import redis
import random

redis_client = redis.Redis(host='localhost', port=6379, db=1)
position_obj = {"url": "https://www.reveliolabs.com/job/97513c3d-b4a4-4bfb-b71e-f95d5482ed14/", "location": "New York, NY", "scraped_on":1721183915}
files = ['../data/test1.jsonl', '../data/test2.jsonl', '../data/test3.jsonl', '../data/test4.jsonl']
data_rows = [5500, 55000, 555000, 8000000]
input_value = input("Select a case (0-3): ")
case = int(input_value)
number_new_ids = round(data_rows[case] / 90)
number_reused_ids = data_rows[case] - number_new_ids

def get_cached_keys(redis_client, count=number_reused_ids):
    all_keys = []
    cursor = '0'

    while cursor != 0 and len(all_keys) < count:
        cursor, keys = redis_client.scan(cursor=cursor, count=count)
        all_keys.extend(keys)
        
    while len(all_keys) < count:
        random_key = redis_client.randomkey()
        if random_key is not None:
            all_keys.append(random_key)

    random_keys = random.sample(all_keys, min(count, len(all_keys)))

    return random_keys

def create_new_keys(num_new_ids):
    new_keys = []
    counter = 0
    while counter < num_new_ids:
        new_key = str(uuid.uuid4())
        new_keys.append(new_key)    
        counter +=1

    return new_keys

def populate_unique_data(keys):
    for key in keys:
        half = int(len(key) / 2)
        first_part = key[:half]
        second_part = key[-half:]
        new_position = position_obj.copy()
        new_position['company'] = first_part
        new_position['title'] = second_part
        unique_data.append(new_position)

unique_data = []
reused_keys = get_cached_keys(redis_client, number_reused_ids)
new_keys = create_new_keys(number_new_ids)

populate_unique_data(reused_keys)
populate_unique_data(new_keys)

for obj in unique_data:
    # Convert byte values to strings (decode bytes to UTF-8 strings)
    cleaned_obj = {k: (v.decode('utf-8') if isinstance(v, bytes) else v) for k, v in obj.items()}
    
    # Write the cleaned object to the file as JSON
    with open(files[case], 'a') as write_file:
        write_file.write(json.dumps(cleaned_obj) + '\n')