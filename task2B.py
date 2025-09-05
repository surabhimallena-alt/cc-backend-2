import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify

app = Flask(__name__)

all_types_url = f"https://pokeapi.co/api/v2/type"
all_types_response = requests.get(all_types_url)
all_types_data = all_types_response.json()

# dictionary with key:value as type_name:index_in_2D_list
# index in 2D list is one less than the type ID
type_list = [all_types_data['results'][index]['name'] for index in range(18)]

damage_multipliers = [['1' for i in range(18)] for i in range(18)]

def fetch_type_data(defender_name):
    global damage_multipliers, type_list

    type_url = f"https://pokeapi.co/api/v2/type/{defender_name}"
    type_response = requests.get(type_url)
    type_data = type_response.json()

    #list comprehension to create list of types that type_name deals damage from
    double_damage_from = [type_data['damage_relations']['double_damage_from'][i]['name'] \
                          for i in range(len(type_data['damage_relations']['double_damage_from']))]
    half_damage_from = [type_data['damage_relations']['half_damage_from'][i]['name'] \
                          for i in range(len(type_data['damage_relations']['half_damage_from']))]
    no_damage_from = [type_data['damage_relations']['no_damage_from'][i]['name'] \
                          for i in range(len(type_data['damage_relations']['no_damage_from']))]
    
    row_index = type_list.index(defender_name)

    for attacker_name in double_damage_from:
        col_index = type_list.index(attacker_name)
        damage_multipliers[row_index][col_index] = '2'

    for attacker_name in half_damage_from:
        col_index = type_list.index(attacker_name)
        damage_multipliers[row_index][col_index] = '1/2'

    for attacker_name in no_damage_from:
        col_index = type_list.index(attacker_name)
        damage_multipliers[row_index][col_index] = '0'


with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(fetch_type_data, type_list)

def both_params():
    global damage_multipliers
    
for row in damage_multipliers:
    print(row)