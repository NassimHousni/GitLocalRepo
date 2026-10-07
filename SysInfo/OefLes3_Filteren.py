import json
import psutil
import platform
import socket
import datetime
import subprocess
import os

def collect_system_info():
    data = {}

    # CPU info
    data["cpu"] = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_processors": psutil.cpu_count(logical=True),
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        "cpu_percent_total": psutil.cpu_percent(interval=0.1),
        "cpu_percent_per_cpu": psutil.cpu_percent(interval=0.1, percpu=True),
    }

    # Memory info
    data["memory"] = psutil.virtual_memory()._asdict()
    data["swap"] = psutil.swap_memory()._asdict()

    # Storage info
    storage = {}
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            storage[part.mountpoint] = {
                "device": part.device,
                "fstype": part.fstype,
                "opts": part.opts,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            }
        except PermissionError:
            continue

    data["storage"] = storage

    # Network info
    net = {}
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    io = psutil.net_io_counters(pernic=True)

    for iface, addr_list in addrs.items():
        net[iface] = {
            "addrs": [a._asdict() for a in addr_list],
            "stats": stats[iface]._asdict() if iface in stats else None,
            "io": io[iface]._asdict() if iface in io else None,
        }

    data["network"] = {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "interfaces": net,
    }

    return data

if __name__ == "__main__":
    info = collect_system_info()

    result = subprocess.run(
        ["powershell", "-Command", "(Get-CimInstance Win32_ComputerSystem).Model"],
        capture_output=True,
        text=True
    )

    system_drive = os.environ["SystemDrive"] + "\\"

        # Find the primary active network interface
    primary_interface = None

    for iface, addr_list in psutil.net_if_addrs().items():
        stats = psutil.net_if_stats().get(iface)

        if stats and stats.isup:
            ipv4 = None

            for addr in addr_list:
                if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                    ipv4 = addr.address

            if ipv4:
                primary_interface = iface
                break

    # Network addresses
    mac_address = None
    ipv4_address = None
    ipv6_address = None
    ipv6_link_local = None

    if primary_interface:
        for addr in psutil.net_if_addrs()[primary_interface]:

            if addr.family == psutil.AF_LINK:
                mac_address = addr.address

            elif addr.family == socket.AF_INET:
                ipv4_address = addr.address

            elif addr.family == socket.AF_INET6:
                if addr.address.lower().startswith("fe80"):
                    ipv6_link_local = addr.address
                else:
                    ipv6_address = addr.address

    # Filter only the requested information
    filtered_info = {
        "computernaam": socket.gethostname(),
        "computermodel": result.stdout.strip(),
        "processor": info["cpu"]["processor"],
        "physical_cores": info["cpu"]["physical_cores"],
        "max_cpu_frequency_mhz": round(info["cpu"]["cpu_freq"]["max"], 2),
        "total_ram_gib": round(info["memory"]["total"] / (1024 ** 3), 2),
        "filesystem": info["storage"][system_drive]["fstype"],
        "storage_capacity_gib": round(
            info["storage"][system_drive]["total"] / (1024 ** 3), 2
        ),
        "mac_address": mac_address,
        "ipv4_address": ipv4_address,
        "ipv6_address": ipv6_address,
        "ipv6_link_local": ipv6_link_local
    }

    print(filtered_info)