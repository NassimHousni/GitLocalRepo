import csv
import os
import glob

# De map met de CSV-bestanden van alle groepsleden
input_folder = os.path.join(os.path.dirname(__file__), "Input")

# Automatisch alle CSV-bestanden in de map zoeken
csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

# De gevonden CSV-bestanden tonen
print("Gevonden CSV-bestanden:", csv_files)

# De kolomnamen moeten voor alle groepsleden hetzelfde zijn
columns = [
    "computernaam",
    "processor",
    "physical_cores",
    "max_cpu_frequency_mhz",
    "total_ram_gib"
]

# Een lege lijst om de gegevens van alle computers te verzamelen
all_computers = []

# Alle CSV-bestanden van de groepsleden inlezen
for csv_file in csv_files:
    with open(csv_file, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        # De gegevens van elke computer toevoegen aan de lijst
        for row in reader:
            computer = {}

            for column in columns:
                computer[column] = row.get(column, "")

            all_computers.append(computer)

# Het gemeenschappelijke CSV-bestand aanmaken
output_file = os.path.join(os.path.dirname(__file__), "combined_system_info.csv")

# Alle computergegevens naar één CSV-bestand schrijven
with open(output_file, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns, delimiter=";")

    writer.writeheader()
    writer.writerows(all_computers)

print("CSV files merged successfully.")

# Hoe zorgen we ervoor dat de kolomnamen hetzelfde zijn?
# We gebruiken voor alle groepsleden dezelfde vijf kolomnamen.
# De lijst 'columns' bepaalt de structuur van het CSV-bestand.

# Wat gebeurt er als gegevens ontbreken?
# Met row.get(column, "") vullen we ontbrekende gegevens
# automatisch aan met een lege waarde.

# Hoe bepalen we welke CSV-bestanden worden ingelezen?
# Met glob.glob() zoeken we automatisch alle CSV-bestanden
# in de map Input.

# Hoe kunnen we later nieuwe computers toevoegen?
# Nieuwe groepsleden plaatsen hun CSV-bestand in de map Input.
# Wanneer we het script opnieuw uitvoeren, worden alle bestanden
# automatisch samengevoegd.

# Afspraken binnen het team:
# Alle CSV-bestanden gebruiken dezelfde kolomnamen en puntkomma (;).
# Elk groepslid gebruikt een eigen bestandsnaam, bijvoorbeeld Nassim.csv.
# De bestanden worden uitgewisseld via de map Input.