from netmiko import ConnectHandler
from getpass import getpass

device = {
    "device_type": "cisco_ios",
    "host": "10.10.20.171",
    "username": "cisco",
        "password": getpass("SSH-wachtwoord: "),
    "secret": getpass("Enable-wachtwoord: "),
}

# Open een SSH-verbinding met de router.
connection = ConnectHandler(**device)

# Schakel over naar de beheerdersmodus.
connection.enable()

# Voer de opdracht uit en toon het resultaat.
output = connection.send_command("show ssh")
print(output)

# Sluit de verbinding.
connection.disconnect()