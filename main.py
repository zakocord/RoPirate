import requests
import json
import socket
import os
import colorama
import pystyle
from pystyle import *
from colorama import Fore
from urllib.parse import urlparse  # ✅ 追加

def load_config(filename="data/config.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

config = load_config()
LIMIT = config["limit"]
min_players = config["server_settings"]["min_players"]
max_players = config["server_settings"]["max_players"]

print (f"""{Fore.RED}
             ........                                                                               
            .,,',''''.                                                               
           .,,,,;,,,;,....                                                         
          .;;;;;;;;;;;;,...                                               
          .,:::;;::;:::. .'                              
     ...'..,::::::::::;..,'..               
   .;ccccc::cccccccccc:;;:,;'                         
   'clllcllllllllllllllllllc'                                     
  'clllllccllllllllllllc:lll,                                                 
 ,looool:.'looooooooooo;.;olc;.                                                                     
'ldoodc.  'odoodoodooodlcooodl.                                                                     
lddddo'   'odddddddddddddddddl.                                                                     
lxxo,.    'dxxxxxxxxxxxdxxxxxc                                                                      
cxxxc.    'xkxxxd;.'c;.'lxxxko'                                                                     
.;lc.     ,xkkkkd.  ;;  .oddddxo,                                                                   
          ,kOOOOx. .do.  .c;,lko'                                                                   
          ,kOOO0x'  c:   .lxxOk'                                                                    
          ,k0000k'  .     ;k00k'                                                                    
          ,OKKKKO'         .,,.                                                                     
          .:cccc;.                                                                                  
{Fore.RESET}""")

place = input(f"{Fore.GREEN}@[+] {Fore.RESET}- PLACE ID~{Fore.BLACK}   ")

API = f"https://games.roblox.com/v1/games/{place}/servers/Public?limit={LIMIT}"

parsed_url = urlparse(API)
hostname = parsed_url.hostname  

ip_address = socket.gethostbyname(hostname)

response = requests.get(API)
if response.status_code == 200:
    print(f"{Fore.GREEN}[+] Connected")
    print(f"""
{Fore.YELLOW}[INFO] {Fore.RESET}
{hostname} : {ip_address}
-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
""")

    data = response.json()

    filtered_servers = [
        server for server in data.get("data", [])
        if min_players <= server.get("playing") <= max_players
    ]

    for server in filtered_servers:
        server_id = server["id"]
        join = f"roblox://placeId={place}&gameInstanceId={server_id}"

        print(f"{Fore.GREEN}[+] {Fore.RESET}succeeded")
        print(f"PLAYER: {Fore.BLUE}{server.get('playing')}/{server.get('maxPlayers')}")
        print(f"Connect URL: {join}")
        os.system("pause")
else:
    print(f"{Fore.RED}[-] ERROR {response.status_code}")
