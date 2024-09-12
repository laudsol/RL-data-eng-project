import json
import uuid

position_obj = {"url": "https://www.reveliolabs.com/job/97513c3d-b4a4-4bfb-b71e-f95d5482ed14/", "location": "New York, NY", "scraped_on":1721183915}
files = ['../data/test1.jsonl', '../data/test2.jsonl', '../data/test3.jsonl', '../data/test4.jsonl']
data_rows = [5500, 55000, 555000, 8000000]
input_value = input("Select a case (0-3): ")
case = int(input_value)
unique_data = []

copy_counter = 0

while copy_counter < data_rows[case] / 90:
    unique_value = str(uuid.uuid4())
    half = int(len(unique_value) / 2)
    first_part = unique_value[:half]
    second_part = unique_value[-half:]
    new_position = position_obj.copy()
    new_position['company'] = first_part
    new_position['title'] = second_part
    unique_data.append(new_position)
    copy_counter += 1

for obj in unique_data:
    data_counter = 0
    while data_counter < 90:
        with open(files[case], 'a') as write_file:
            write_file.write(json.dumps(obj) + '\n')    
        data_counter += 1