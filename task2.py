import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor

def fetch_pokemon_data(name):
    poke_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{name}"

    poke_response = requests.get(poke_url)
    species_response = requests.get(species_url)

    poke_data = poke_response.json()
    species_data = species_response.json()

    return {
        'name': poke_data['name'],
        'id': poke_data['id'],
        'abilities': poke_data['abilities'],
        'type': poke_data['types'],
        'is_legendary': species_data['is_legendary'],
        'is_mythical': species_data['is_mythical']
    }

data = {}
with open("pokemon.txt") as f:
    pokemon_names = [line.strip() for line in f]

with ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(fetch_pokemon_data, pokemon_names)

for result in results:
    data[result['name']] = {
        'id': result['id'],
        'abilities': result['abilities'],
        'type': result['type'],
        'is_legendary': result['is_legendary'],
        'is_mythical': result['is_mythical']
    }

if len(sys.argv) < 2:
    print("Usage: python write_json.py <filename.json>")
    sys.exit(1)

# Get the filename from the command line
filename = sys.argv[1]

# Optional: Add .json extension if not present
if not filename.endswith(".json"):
    filename += ".json"

# Write the dictionary to the file (create or overwrite)
with open(filename, "w") as f:
    json.dump(data, f, indent=4)
