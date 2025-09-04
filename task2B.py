import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor

def fetch_type_data(type_name):
    type_url = f"https://pokeapi.co/api/v2/type/{type_name}"
    type_response = requests.get(type_url)
    type_data = type_response.json()
    double_damage_from = [type_data['damage_relations']['double_damage_from'][i]['name'] \
                          for i in range(len(type_data['damage_relations']['double_damage_from']))]
    half_damage_from = [type_data['damage_relations']['half_damage_from'][i]['name'] \
                          for i in range(len(type_data['damage_relations']['half_damage_from']))]
    no_damage_from = [type_data['damage_relations']['no_damage_from'][i]['name'] \
                          for i in range(len(type_data['damage_relations']['no_damage_from']))]
    print(double_damage_from)
    print(half_damage_from)
    print(no_damage_from)

fetch_type_data('normal')

all_types_url = f"https://pokeapi.co/api/v2/type"
all_types_response = requests.get(all_types_url)
all_types_data = all_types_response.json()

# dictionary with key:value as type_name:index_in_2D_list
# index in 2D list is one less than the type ID
type_dict = {all_types_data['results'][index]['name']:index for index in range(19)}

damage_multipliers = [['1' for i in range(19)] for i in range(19)]
