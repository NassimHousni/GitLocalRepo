from netmiko import ConnectHandler
from getpass import getpass
# Bewaar de verbindingsgegevens in variabelen.
v_device_type = "cisco_ios"
v_host = "10.10.20.171"
v_ssh_port = 22
v_username = "cisco"
v_password = getpass("SSH-wachtwoord: ")
v_secret = getpass("Enable-wachtwoord: ")
# Verzamel de variabelen in één dictionary.
device = {
    "device_type": v_device_type,
    "host": v_host,
    "port": v_ssh_port,
    "username": v_username,
    "password": v_password,
    "secret": v_secret,
}

# Maak verbinding en schakel over naar de beheerdersmodus.
connection = ConnectHandler(**device)
connection.enable()

# Vraag de SSH-verbindingen op en toon het resultaat.
output = connection.send_command("show version")
print(output)

# Sluit de verbinding.
connection.disconnect()

# Zoek de routernaam in de ontvangen tekst.
hostname = "Onbekend"

for line in output.splitlines():
    if " uptime is " in line:
        hostname = line.split()[0]

print("Hostname:", hostname)
# Zoek het serienummer in de ontvangen tekst.
serial = "Onbekend"

for line in output.splitlines():
    if "Processor board ID " in line:
        serial = line.split()[-1]

print("Serienummer:", serial)
# Zoek de IOS-versie in de ontvangen tekst.
ios_version = "Onbekend"

for line in output.splitlines():
    if line.startswith("Cisco IOS Software") and "Version " in line:
        ios_version = line.split("Version ", 1)[1].split(",", 1)[0]

print("IOS-versie:", ios_version)
# Zoek de platformbeschrijving van deze virtuele router.
model = "Onbekend"

for line in output.splitlines():
    if " processor with " in line:
        model = line.split(" processor with ", 1)[0]

print("Model/platform:", model)
