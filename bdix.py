import json
import time
import requests
import threading
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor


def read_servers_json():
    try:
        with open('server.json', 'r') as file:
            data = json.load(file)
            return data.get('ftp', []), data.get('tv', []), data.get('others', [])
    except FileNotFoundError:
        print(f"File 'server.json' not found.")
        return [], [], []

ftp,tv,others = read_servers_json()


# Create a lock for printing
print_lock = threading.Lock()
opo = False

def td(text: str, length=40, d='-'):
    text_length = len(text)
    padding_length = max(0, length - text_length) - 1
    padding = ' ' + d * padding_length
    decorated_text = f"{text}{padding}"
    return decorated_text

def check_server(server):
    try:
        start_time = time.time()
        response = requests.get(server, timeout=5)
        latency = int((time.time() - start_time) * 1000)  # Calculating latency in milliseconds
        if response.status_code == 200:
            with print_lock:
                tdr = td(f"|  [~]- Alive and Ping is - {latency}ms") + td(f" | {server}", 109) + '|'
                print(colored(tdr, 'green'))
        elif response.status_code == 301 or response.status_code == 302:
            with print_lock:
                tdr = td(f"|  [?]- May contain threat - {latency}ms") + td(f" | {server}", 109) + '|'
                print(colored(tdr, 'magenta'))
        else:
            with print_lock:
                tdr = td(f"|  [d]- Dead-   ping time - {latency}ms") + td(f" | {server}", 109) + '|'
                if not opo:print(colored(tdr, 'red'))
    except requests.ConnectionError:
        with print_lock:
            tdr = td(f"|  [d]- Dead-   ping time - {latency}ms") + td(f" | {server}", 109) + '|'
            if not opo:print(colored(tdr, 'red'))
    except requests.Timeout:
        with print_lock:
            tdr = td(f"|  [!]- N sur (Timed out) - {latency}ms") + td(f" | {server}", 109) + '|'
            if not opo:print(colored(tdr, 'yellow'))
    except Exception as e:
        with print_lock:
            tdr = td(f"|  [!]- N sur ({e}) - {latency}ms") + td(f" | {server}", 109) + '|'
            if not opo:print(colored(tdr, 'yellow'))



def executor1():
    global opo
    servers = ftp + tv + others
    opo = True
    t=15
    print(colored(f"Checking ALL servers in data set, Also Running on 15 threads and debug is on:", 'blue'))
    print("\n")
    print(colored(" ____________________________________________________________________________________________________________________________________________________ ", "blue"))
    print(colored("| FTP SERVER CONDITION WITH PING STATUS  |                                     FTP SERVER LINKS ACCORDING CONDITION                                  |", "blue"))
    print(colored("|----------------------------------------|-----------------------------------------------------------------------------------------------------------|", "blue"))
    with ThreadPoolExecutor(max_workers=t) as executor:
        executor.map(check_server, servers)


def executor2():
    global opo
    
    print("[1] Check TV servers")
    print("[2] Check ALL servers")
    print("[3] Check FTP servers")
    print("[4] Check Others servers")
    while True:
        x = input("enter your choice (blank for FTP):")
        if x =='1':
            servers = tv
        elif x =='2':
            servers = ftp + tv + others
        elif x =='3':
            servers = ftp
        elif x =='4':
            servers = others
        else:
            print("Wrong input, Try Again\n")
            continue
        break
    d = ['None','TV','ALL','FTP','OTHER']
    xv = int(x)
    # Check servers using ThreadPoolExecutor
    print(colored(f"Checking {d[xv]} servers:", 'blue'))
    while True:
        try:
            t = int(input("\nEnter Threadings : "))
        except:
            print("Wrong input, Try Again\n")
            continue
        break
    only_print_ok = input("\nOnly Print Ok Sites (y/n) : ")
    opo = only_print_ok=='y' or only_print_ok=='Y'
    print("\n")
    print(colored(" ____________________________________________________________________________________________________________________________________________________ ", "blue"))
    print(colored("| FTP SERVER CONDITION WITH PING STATUS  |                                     FTP SERVER LINKS ACCORDING CONDITION                                  |", "blue"))
    print(colored("|----------------------------------------|-----------------------------------------------------------------------------------------------------------|", "blue"))
    with ThreadPoolExecutor(max_workers=t) as executor:
        executor.map(check_server, servers)