import os
from os.path import sep
import sys

WIN = sys.platform.startswith("win")


# Detect OS platform.


def ping(hostname):
    response = os.system(f"ping -{'n' if WIN else 'c'} 1 {hostname}")

    if response == 0:
        print(hostname, 'is up!')
    else:
        print(hostname, 'is down!')


# Ping the host, use -n if running from Linux, -c if ran from Windows

def run():
    for host in open(f".{sep}hosts.txt", "r").read().splitlines():
        print(f"Host gevonden in TXT-file: {host}")
        ping(host)
        print("\n")

