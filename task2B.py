import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor

def fetch_type_data(type_name):
    type_url = f"https://pokeapi.co/api/v2/type/{type_name}"
    type_response = requests.get(type_url)
    type_data = type_response.json()
    pass

all_types_url = f"https://pokeapi.co/api/v2/type"
all_types_response = requests.get(all_types_url)
all_types_data = all_types_response.json()

# dictionary with key:value as type_name:type_id
type_dict = {all_types_data['results'][index]['name']:index+1 for index in range(19)}

print(type_dict)