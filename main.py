import requests
import json
import socket
import os
import colorama
import logging
from pystyle import *
from colorama import Fore
from urllib.parse import urlparse
#d

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def load_config(filename="data/config.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"{filename} NOT FOUND")
        exit(1)
    except json.JSONDecodeError:
        logger.error(f"{filename} is incorrect.")
        exit(1)

def get_ip_from_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        logger.error(f"{hostname} Grab Error")
        exit(1)

def server_filter(place, limit, low_, max_):
    API = f"https://games.roblox.com/v1/games/{place}/servers/Public?limit={limit}"
    try:
        response = requests.get(API)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"API ERROR: {e}")
        exit(1)

    data = response.json()
    logger.debug(f"API Response: {json.dumps(data, indent=2)}") 

    return [
        server for server in data.get("data", [])
        if low_ <= server.get("playing") <= max_
    ]

def display(filtered_servers, place):
    if not filtered_servers:
        logger.warning("No servers matching your criteria were found")
        return

    for server in filtered_servers:
        server_id = server["id"]
        join_url = f"roblox://placeId={place}&gameInstanceId={server_id}"

        print(f"{Fore.GREEN}[+] {Fore.RESET}succeeded")
        print(f"PLAYER: {Fore.BLUE}{server.get('playing')}/{server.get('maxPlayers')}")
        print(f"Connect URL: {join_url}")

def main():
    print (f""" {Fore.RED}
                      /$$$$$$$            /$$$$$$$  /$$                      /$$              
                     | $$__  $$          | $$__  $$|__/                     | $$              
                     | $$  \ $$  /$$$$$$ | $$  \ $$ /$$  /$$$$$$  /$$$$$$  /$$$$$$    /$$$$$$ 
                     | $$$$$$$/ /$$__  $$| $$$$$$$/| $$ /$$__  $$|____  $$|_  $$_/   /$$__  $$
                     | $$__  $$| $$  \ $$| $$____/ | $$| $$  \__/ /$$$$$$$  | $$    | $$$$$$$$
                     | $$  \ $$| $$  | $$| $$      | $$| $$      /$$__  $$  | $$ /$$| $$_____/
                     | $$  | $$|  $$$$$$/| $$      | $$| $$     |  $$$$$$$  |  $$$$/|  $$$$$$$
                     |__/  |__/ \______/ |__/      |__/|__/      \_______/   \___/   \_______/

{Fore.RESET}""")

    place = input(f"@{Fore.YELLOW}[INPUT] {Fore.RESET}- PLACE ID~{Fore.BLACK}   ")
    if not place.isdigit():
        print(f"{Fore.RED} [-] Invaild Place ID")
        logging.error("[-] - invaild Place id")
        exit(1)
    place = int(place)

    config = load_config()
    LIMIT = config.get("limit", 100)
    low_ = config["server_settings"]["min_players"]
    max_ = config["server_settings"]["max_players"]

    API = f"https://games.roblox.com/v1/games/{place}/servers/Public?limit={LIMIT}"
    parsed_url = urlparse(API)
    hostname = parsed_url.hostname
    ip_address = get_ip_from_hostname(hostname)

    logger.info(f"Connected to {hostname} : {ip_address}")
    print (f"""{Fore.YELLOW} [INFO]
           Connect: {hostname} : {ip_address} {Fore.RESET}
           """)

    filtered_servers = server_filter(place, LIMIT, low_, max_)
    display(filtered_servers, place)

if __name__ == "__main__":
    main()
