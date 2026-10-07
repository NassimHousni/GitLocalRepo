import json
import sys
import os

# Cherche OefLes3_Filteren.py dans le dossier Filteren
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Filteren"))

from OefLes3_Filteren import collect_system_info

# Récupérer les informations du système
info = collect_system_info()

# Garder les informations demandées
filtered_info = {
    "computernaam": info["network"]["hostname"],
    "processor": info["cpu"]["processor"],
    "physical_cores": info["cpu"]["physical_cores"],
    "max_cpu_frequency_mhz": info["cpu"]["cpu_freq"]["max"],
    "total_ram_gib": round(info["memory"]["total"] / (1024 ** 3), 2)
}

# Convertir la dictionary Python en JSON
json_data = json.dumps(filtered_info, indent=4)

print(json_data)

# Chemin du fichier JSON dans le même dossier que ce script
json_file = os.path.join(os.path.dirname(__file__), "system_info.json")

# Sauvegarder les données dans un fichier JSON
with open(json_file, "w") as file:
    json.dump(filtered_info, file, indent=4)

# Relire le fichier JSON comme une Python dictionary
with open(json_file, "r") as file:
    loaded_info = json.load(file)

print(loaded_info)

# Vérifier si les données correspondent
if filtered_info == loaded_info:
    print("The data matches the original dictionary.")
else:
    print("The data does not match the original dictionary.")

# Een Python dictionary is een datastructuur die in Python wordt gebruikt.
# JSON is een tekstformaat om gegevens op te slaan of uit te wisselen.
# Een Python dictionary kan met json.dumps() of json.dump() naar JSON worden omgezet.
# JSON kan met json.loads() of json.load() terug naar een Python dictionary worden omgezet.