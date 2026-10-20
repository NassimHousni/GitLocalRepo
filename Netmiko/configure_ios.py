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
# Pas de gevraagde instellingen toe.
config_commands = [
    "service password-encryption",
    "banner motd #Unauthorized access is prohibited#",
]

output = connection.send_config_set(config_commands)
print(output)

# Bewaar de instellingen voor de volgende herstart.
save_output = connection.save_config()
print(save_output)

# Sluit de verbinding.
connection.disconnect()


