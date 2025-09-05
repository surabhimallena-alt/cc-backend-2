import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify


all_types_url = f"https://pokeapi.co/api/v2/type"
all_types_response = requests.get(all_types_url)
all_types_data = all_types_response.json()

# dictionary with key:value as type_name:index_in_2D_list
# index in 2D list is one less than the type ID
type_list = [all_types_data['results'][index]['name'] for index in range(18)]
#['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost', \
# 'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy']

damage_multipliers = [[1 for i in range(18)] for i in range(18)]

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
        damage_multipliers[row_index][col_index] = 2

    for attacker_name in half_damage_from:
        col_index = type_list.index(attacker_name)
        damage_multipliers[row_index][col_index] = 0.5

    for attacker_name in no_damage_from:
        col_index = type_list.index(attacker_name)
        damage_multipliers[row_index][col_index] = 0


with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(fetch_type_data, type_list)

app = Flask(__name__)

def both_params(attacker, defender):
    global damage_multipliers, type_list

    row_index = type_list.index(defender)
    col_index = type_list.index(attacker)
    multiplier = damage_multipliers[row_index][col_index]
    
    return {'attacker':attacker, 'defender':defender, 'multiplier':multiplier}

def attacker_param(attacker):
    global damage_multipliers, type_list

    col_index = type_list.index(attacker)
    multiplier_list = [damage_multipliers[i][col_index] for i in range(len(damage_multipliers))]
    to_defenders = {type_list[i]:multiplier_list[i] for i in range(len(damage_multipliers))}
    return {
        'attacker':attacker,
        'to_defenders':to_defenders
    }

def defender_param(defender):
    global damage_multipliers, type_list

    row_index = type_list.index(defender)
    multiplier_list = [damage_multipliers[row_index][i] for i in range(len(damage_multipliers))]
    from_attackers = {type_list[i]:multiplier_list[i] for i in range(len(damage_multipliers))}
    return {
        'defender':defender,
        'from_attackers':from_attackers
    }


@app.route('/')
def handle_request():
    global damage_multipliers, type_list

    attacker = request.args.get('attacker')
    defender = request.args.get('defender')

    if not attacker and not defender:
        return jsonify({"error": "Either attacker or defender must be provided"}), 400
    
    if attacker and attacker not in type_list:
        return jsonify({"error": "Invalid attacker type"}), 400
    
    if defender and defender not in type_list:
        return jsonify({"error": "Invalid defender type"}), 400

    if attacker and defender:
        response = both_params(attacker, defender)
    elif attacker and not defender:
        response = attacker_param(attacker)
    elif defender and not attacker:
        response = defender_param(defender)

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8000, debug=True)