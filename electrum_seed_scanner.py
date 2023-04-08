#!/usr/bin/env python3

import io
import json
import os.path
import subprocess
import concurrent.futures
import BIP39
import pyfiglet

def brute_force():
    word = BIP39.WORDLIST
    start = "abandon"
    for layer1 in range(len(word)):
        phrase1 = f"minor zone pool {word[layer1]} remain combine {start} claw medal settle grace capable"
        yield phrase1
        for layer2 in range(len(word)):
            phrase2 = f"minor zone pool {word[layer1]} remain combine {word[layer2]} claw medal settle grace capable"
            yield phrase2

def process_seed_phrase(seed_phrase, index, my_key, wallet_path):
    command = ["electrum", "restore", "-w", wallet_path, seed_phrase]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        return

    if os.path.exists(wallet_path):
        with io.open(wallet_path, 'r') as file:
            data = json.load(file)

        mnemonic = data["keystore"]["seed"]
        master_key = data["keystore"]["xpub"]

        if my_key == master_key:
            with open("/home/rushmi0/.electrum/ビットコイン会った.txt", "a") as f:
                f.write(f"{index + 1} | {mnemonic}\n")
                f.write(f"{index + 1} | {master_key}\n\n")

def main():
    my_key = "zpub6nhhoBvkc6pNgU3JPwobardNLniafeTGnBkxrw8XLv3DeB24W2ycBD68dNciURmdUdqkbggGRCsSNCHg6UJCnYy4tA1GKMa1ZcRGK4Rpjth"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, seed_phrase in enumerate(brute_force()):
            # print(f'{i + 1} | {seed_phrase}')
            wallet_path = f"/home/rushmi0/.electrum/electrum_wallet/restore_{i}.json"
            executor.submit(process_seed_phrase, seed_phrase, i, my_key, wallet_path)

if __name__ == "__main__":
    result = pyfiglet.figlet_format("Scanning", font="big")
    print(result)
    main()
