import http.client
import json

# Step 1: Prompt the user for the authorization token
authorization_token = input("Please enter your authorization token: ")

# Step 2: Make the API request
conn = http.client.HTTPSConnection("u.otogame.net")
payload = ''
headers = {
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Authorization': f'Bearer {authorization_token}',  # Use the input token here
    'Accept': '*/*',
    'Host': 'u.otogame.net',
    'Connection': 'keep-alive'
}

# Make the GET request to the API
conn.request("GET", "/api/game/ongeki/rating", payload, headers)
res = conn.getresponse()
data = res.read()

# Step 3: Parse the API response directly
api_data = json.loads(data.decode("utf-8"))  # Parse the response as JSON

# Step 4: Parse the '1.txt' file and create mappings of song names to numbers
name_to_number_below_2000 = {}
name_to_number_8000 = {}

# Using relative path for 1.txt (assuming it's in the same directory as this script)
with open('1.txt', 'r', encoding='utf-8') as file:
    for line in file:
        name, number = line.strip().split('\t')
        number = int(number)  # Convert number to integer for comparison
        if number < 2000:  # Store those less than 2000
            name_to_number_below_2000[name] = number
        if number >= 8000:  # Store those starting from 8000
            name_to_number_8000[name] = number

# Step 5: Prepare output for best_rating_list
best_rating_list = api_data['data']['best_rating_list']
output_best_rating = []

for item in best_rating_list:
    song_name = item['music']['name']
    difficulty = item['difficulty']
    score = item['score']

    # Check for difficulty == 3 and < 2000
    if difficulty <= 3 and song_name in name_to_number_below_2000:
        song_number = name_to_number_below_2000[song_name]
        output_best_rating.append(f"{song_number}:{difficulty}:{score}")  # Use mapping for <2000

    # Check for difficulty == 10
    elif difficulty == 10 and song_name in name_to_number_8000:
        song_number = name_to_number_8000[song_name]
        output_best_rating.append(f"{song_number}:{difficulty}:{score}")  # Use mapping starting from 8000

# Step 6: Prepare output for best_new_rating_list
best_new_rating_list = api_data['data']['best_new_rating_list']
output_best_new_rating = []

for item in best_new_rating_list:
    song_name = item['music']['name']
    difficulty = item['difficulty']
    score = item['score']

    # Check for difficulty == 3 and < 2000
    if difficulty <= 3 and song_name in name_to_number_below_2000:
        song_number = name_to_number_below_2000[song_name]
        output_best_new_rating.append(f"{song_number}:{difficulty}:{score}")  # Use mapping for <2000

    # Check for difficulty == 10
    elif difficulty == 10 and song_name in name_to_number_8000:
        song_number = name_to_number_8000[song_name]
        output_best_new_rating.append(f"{song_number}:{difficulty}:{score}")  # Use mapping starting from 8000

# Step 7: Update the JSON file with b30 and n15

# Load the existing JSON structure
with open('1.json', 'r', encoding='utf-8') as json_file:
    existing_data = json.load(json_file)

# Update the 'b30' and 'n15' fields
for item in existing_data['userGeneralDataList']:
    if item['propertyKey'] == 'rating_base_best':
        item['propertyValue'] = ','.join(output_best_rating)  # Replace b30 with output_best_rating
    elif item['propertyKey'] == 'rating_base_new_best':
        item['propertyValue'] = ','.join(output_best_new_rating)  # Replace n15 with output_best_new_rating

# Step 8: Print or Save the modified JSON
with open('1_modified.json', 'w', encoding='utf-8') as json_file:
    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

# Optionally, print the modified result
print(json.dumps(existing_data, ensure_ascii=False, indent=4))
