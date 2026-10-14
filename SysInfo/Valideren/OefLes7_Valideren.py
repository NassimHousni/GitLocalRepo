import os
import sys
import csv

# De functie importeren uit oefening 3
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Filteren"))

from OefLes3_Filteren import collect_system_info

# De actuele systeeminformatie verzamelen
info = collect_system_info()

# Het CSV-bestand van oefening 6 openen
csv_file = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Samenvoegen",
    "combined_system_info.csv"
)

# De opgeslagen computergegevens inlezen
with open(csv_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:
        if row["computernaam"] == info["network"]["hostname"]:
            saved_info = row
            break
    else:
        saved_info = None

print("Opgeslagen gegevens:", saved_info)

# De opgeslagen gegevens vergelijken met de actuele systeeminformatie
if saved_info is not None:

    current_info = {
        "computernaam": info["network"]["hostname"],
        "processor": info["cpu"]["processor"],
        "total_ram_gib": round(info["memory"]["total"] / (1024 ** 3), 2)
    }

    # De gegevens controleren
    for key, value in current_info.items():

        if str(value) == saved_info.get(key, ""):
            print(key, ": OK")
        else:
            print(key, ": Verschil gevonden")
            print("Opgeslagen:", saved_info.get(key, ""))
            print("Actueel:", value)

else:
    print("Computer niet gevonden in het CSV-bestand.")

# De actuele netwerk- en opslaginformatie ophalen
wifi = info["network"]["interfaces"].get("Wi-Fi", {})

ipv4_address = ""
mac_address = ""

for address in wifi.get("addrs", []):
    if address["family"].name == "AF_INET":
        ipv4_address = address["address"]

    elif address["family"].name == "AF_LINK":
        mac_address = address["address"]

# De opslagcapaciteit van schijf C: berekenen in GiB
storage_capacity_gib = round(
    info["storage"]["C:\\"]["total"] / (1024 ** 3), 2
)

print("IPv4:", ipv4_address)
print("MAC:", mac_address)
print("Storage (GiB):", storage_capacity_gib)

# De ontbrekende gegevens in het CSV-bestand controleren
extra_info = {
    "ipv4_address": ipv4_address,
    "mac_address": mac_address,
    "storage_capacity_gib": storage_capacity_gib
}

if saved_info is not None:
    for key, value in extra_info.items():
        if key not in saved_info or saved_info[key] == "":
            print(key, ": Ontbreekt in CSV")
        elif str(value) == saved_info[key]:
            print(key, ": OK")
        else:
            print(key, ": Verschil gevonden")
            print("Opgeslagen:", saved_info[key])
            print("Actueel:", value)

# Resultaten van de validatie:
# De computernaam, processor en hoeveelheid RAM komen overeen
# met de actuele configuratie van mijn computer.

# Het IPv4-adres, MAC-adres en de opslagcapaciteit ontbreken
# in het CSV-bestand van oefening 6.
# Deze gegevens werden niet opgenomen in de oorspronkelijke
# CSV-structuur. Daarom kunnen we ze nog niet vergelijken.

# Welke controles kunnen we automatisch uitvoeren met Python?
# Python kan de computernaam, processor en RAM controleren.
# Ook het IP-adres, MAC-adres en de opslagcapaciteit kunnen
# automatisch worden opgehaald en vergeleken.

# Mogelijke verschillen:
# Een IP-adres kan veranderen wanneer we van netwerk wisselen.
# Een computer kan meerdere netwerkinterfaces en MAC-adressen hebben.
# De opslagcapaciteit kan verschillen door de gebruikte eenheden
# (GB of GiB) of doordat meerdere schijven aanwezig zijn.

# Een volledig CSV-bestand maken voor de validatie
validation_file = os.path.join(
    os.path.dirname(__file__),
    "system_info_validation.csv"
)

validation_info = {
    "computernaam": info["network"]["hostname"],
    "processor": info["cpu"]["processor"],
    "total_ram_gib": round(info["memory"]["total"] / (1024 ** 3), 2),
    "ipv4_address": ipv4_address,
    "mac_address": mac_address,
    "storage_capacity_gib": storage_capacity_gib
}

# Het CSV-bestand alleen maken als het nog niet bestaat
if not os.path.exists(validation_file):
    with open(validation_file, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=validation_info.keys(), delimiter=";")
        writer.writeheader()
        writer.writerow(validation_info)

print("Validatiebestand is klaar.")

# De opgeslagen gegevens vergelijken met de actuele configuratie
with open(validation_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:
        for key, value in validation_info.items():

            if row[key] == str(value):
                print(key, ": OK")
            else:
                print(key, ": Verschil gevonden")
                print("Opgeslagen:", row[key])
                print("Actueel:", value)