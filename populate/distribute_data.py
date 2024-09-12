import json
import uuid
import numpy as np
import random

position_obj = {"url": "https://www.reveliolabs.com/job/97513c3d-b4a4-4bfb-b71e-f95d5482ed14/", "location": "New York, NY", "scraped_on": 1721183915}

files = ['../data/test1.jsonl', '../data/test2.jsonl', '../data/test3.jsonl', '../data/test4.jsonl']

data_rows = [5500, 55000, 555000, 8000000]

input_value = input("Select a case (0-3): ")
case = int(input_value)

total_rows = data_rows[case]
unique_rows = round(data_rows[case] / 90)

unique_data = []
for _ in range(unique_rows):
    unique_value = str(uuid.uuid4())
    half = int(len(unique_value) / 2)
    first_part = unique_value[:half]
    second_part = unique_value[-half:]
    new_position = position_obj.copy()
    new_position['company'] = first_part
    new_position['title'] = second_part
    unique_data.append(new_position)

mean = total_rows // unique_rows  # Mean frequency of each unique element
std_dev = mean // 5  # Standard deviation for variability

frequencies = np.random.normal(mean, std_dev, unique_rows)

frequencies = np.abs(frequencies).astype(int)  # Ensure positive values
total_sum = np.sum(frequencies)

frequencies = np.round(frequencies * (total_rows / total_sum)).astype(int)

final_list = []
for obj, freq in zip(unique_data, frequencies):
    final_list.extend([obj] * freq)

random.shuffle(final_list)

output_file = files[case]
with open(output_file, 'a') as write_file:
    for obj in final_list:
        write_file.write(json.dumps(obj) + '\n')

print(f"Generated {total_rows} rows and written to {output_file}")
