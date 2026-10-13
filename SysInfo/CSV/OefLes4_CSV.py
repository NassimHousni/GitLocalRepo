import csv
import sys
import os

# De functie importeren uit de vorige oefening
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Filteren"))

from OefLes3_Filteren import collect_system_info

# Systeeminformatie verzamelen
info = collect_system_info()

# De systeeminformatie filteren voor het CSV-bestand
filtered_info = {
    "computernaam": info["network"]["hostname"],
    "processor": info["cpu"]["processor"],
    "physical_cores": info["cpu"]["physical_cores"],
    "max_cpu_frequency_mhz": info["cpu"]["cpu_freq"]["max"],
    "total_ram_gib": round(info["memory"]["total"] / (1024 ** 3), 2)
}

# Het CSV-bestand opslaan in de map CSV
csv_file = os.path.join(os.path.dirname(__file__), "system_info.csv")

# De dictionary naar een CSV-bestand schrijven
with open(csv_file, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=filtered_info.keys(), delimiter=";")

    writer.writeheader()
    writer.writerow(filtered_info)

print("CSV file created successfully.")

# Het CSV-bestand opnieuw inlezen
with open(csv_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:
        print(row)

# We gebruiken een puntkomma (;) als scheidingsteken,
# zodat het CSV-bestand correct kan worden geopend in Excel.

# Ontbrekende informatie kan als een lege cel worden opgeslagen.

# Een computer kan meerdere disks of netwerkinterfaces hebben.
# Deze kunnen in aparte kolommen of in meerdere rijen worden opgeslagen.

# We gebruiken UTF-8 met BOM (utf-8-sig) voor een goede
# weergave van speciale tekens in Excel.

# Met csv.DictWriter schrijven we de dictionary naar CSV.
# Met csv.DictReader lezen we het CSV-bestand opnieuw in.