import json

company_colors = ['black', 'blue', 'red']
company_products = ['hat', 'box', 'consultants', 'partners', 'corp', 'health', 'services', 'inc', 'metals', 'chemicals', 'logistics']
postion_title = ['jr', 'mid', 'sr']
postion_role = ['doctor', 'lawyer', 'engineer', 'teacher', 'cook', 'accountant', 'driver', 'technician', 'salesperson', 'operator', 'thinker']
position_obj = {"url": "https://www.reveliolabs.com/job/97513c3d-b4a4-4bfb-b71e-f95d5482ed14/", "location": "New York, NY", "scraped_on":1721183915}

companies = []
positions = []
unique_data = []

for color in company_colors:
    for product in company_products:
        combo = color + ' ' + product
        companies.append(combo)

for title in postion_title:
    for role in postion_role:
        combo = title + ' ' + role
        positions.append(combo)


for company in companies:
    for position in positions:
        new_position = position_obj.copy()
        new_position['company'] = company
        new_position['title'] = position
        unique_data.append(new_position)

for obj in unique_data:
    counter = 0
    while counter < 500:
        with open('./data/test3.jsonl', 'a') as write_file:
            write_file.write(json.dumps(obj) + '\n')    
        counter += 1