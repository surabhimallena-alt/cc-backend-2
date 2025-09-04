import requests
import json

pokemon = open("pokemon.txt", "r")
data = {}

for line in pokemon:
    poke_url = f"https://pokeapi.co/api/v2/pokemon/{line.strip()}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{line.strip()}"
    
    poke_response = requests.get(poke_url)
    species_response = requests.get(species_url)

    poke_data = poke_response.json()
    species_data = species_response.json()

    poke_name = poke_data['name']
    poke_id = poke_data['id']
    poke_abilities = poke_data['abilities']
    poke_type = poke_data['types']
    is_legendary = species_data['is_legendary']
    is_mythical = species_data['is_mythical']

    poke_data = {
        'id':poke_id, 
        'abilities':poke_abilities, 
        'type':poke_type, 
        'is_legendary':is_legendary, 
        'is_mythical':is_mythical
        }
    
    data[poke_name] = poke_data

print(data)

    