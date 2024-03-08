
#                      © All Right Reserved Hacker-K ®

import socket
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pyfiglet import Figlet
import requests

INTEL_X_API_KEY = "d0b5f781-7c96-4299-8544-5dd62b4c3ba2"

def is_port_open(ip_address, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip_address, port))
            return result == 0
    except Exception as e:
        print(f"Error occurred while checking port {port} on {ip_address}: {str(e)}")
        return False

def read_ip_addresses_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            ip_addresses = file.read().splitlines()
        return ip_addresses
    except Exception as e:
        print(f"Error occurred while reading IP addresses from {file_name}: {str(e)}")
        return []

def get_device_info(ip):
    try:
        url = f"https://api.intelx.io/ipinfo?ip={ip}"
        headers = {"x-key": INTEL_X_API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve device info for {ip}. Status code: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error occurred while retrieving device info for {ip}: {str(e)}")
        return {}

def find_intel_x_bots():
    try:
        ip_addresses = read_ip_addresses_from_file("IP_address.txt")
        if not ip_addresses:
            print("No IP addresses found in the file.")
            return

        print_banner("K SSH-tel-Port-Finder")
        print("Scanning for potential Telnet or SSH bots...")

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            for ip in ip_addresses:
                futures.append(executor.submit(check_ip, ip))
            for future in futures:
                result = future.result()
                if result:
                    print_device_info(result)
    except Exception as e:
        print("Error occurred:", str(e))

def check_ip(ip):
    result = {}
    if is_port_open(ip, 23):
        result['ip'] = ip
        result['open_ports'] = ['Telnet (23)']
        result['device_info'] = get_device_info(ip)
    elif is_port_open(ip, 22):
        result['ip'] = ip
        result['open_ports'] = ['SSH (22)']
        result['device_info'] = get_device_info(ip)
    return result if result else None

def print_banner(text):
    f = Figlet(font='slant')
    banner = f.renderText(text)
    print(banner)

def print_device_info(device):
    print(f"Potential Telnet or SSH bot found at: {device['ip']} - Open Ports: {device['open_ports']}")
    if device['device_info']:
        print("Device Info:")
        for key, value in device['device_info'].items():
            print(f"{key}: {value}")

# Run the function to find Telnet or SSH bots
find_intel_x_bots()

#              © All Right Reserved Hacker-K ®
