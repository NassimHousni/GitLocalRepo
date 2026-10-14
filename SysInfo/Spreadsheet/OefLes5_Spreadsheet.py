import os
from openpyxl import Workbook

# Een nieuw Excel-werkboek aanmaken
wb = Workbook()

# Het actieve werkblad selecteren
ws = wb.active

# Het werkblad een naam geven
ws.title = "System Info"

import csv

# Het CSV-bestand van oefening 4 openen
csv_file = os.path.join(os.path.dirname(__file__), "..", "CSV", "system_info.csv")

# De gegevens uit het CSV-bestand lezen
with open(csv_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file, delimiter=";")

    for row in reader:
        ws.append(row)
        # Het Excel-bestand opslaan in de map Spreadsheet
excel_file = os.path.join(os.path.dirname(__file__), "system_info.xlsx")

# Het werkboek opslaan als Excel-bestand
wb.save(excel_file)

print("Excel file created successfully.")

# Verschil tussen CSV en Excel:
# Een CSV-bestand bevat gegevens in tekstvorm, gescheiden door een scheidingsteken.
# Een Excel-bestand (.xlsx) kan ook opmaak, formules en meerdere werkbladen bevatten.

# Extra mogelijkheden van Excel:
# In Excel kunnen we kleuren, tabellen, grafieken en formules gebruiken.

# Wanneer gebruiken we CSV of Excel?
# CSV is handig om gegevens eenvoudig uit te wisselen tussen programma's.
# Excel is beter wanneer we gegevens willen opmaken, analyseren of presenteren.

# Voor deze oefening gebruiken we openpyxl om een Excel-bestand te maken.
# We gebruiken dezelfde gegevens en kolomnamen als in het CSV-bestand.