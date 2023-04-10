#!/usr/bin/env python3

import io
import json
import os.path
import subprocess
import BIP39
import pyfiglet

def main():
    _key_ = "zpub6nhhoBvkc6pNgU3JPwobardNLniafeTGnBkxrw8XLv3DeB24W2ycBD68dNciURmdUdqkbggGRCsSNCHg6UJCnYy4tA1GKMa1ZcRGK4Rpjth"

    stack = []
    word = BIP39.WORDLIST
    for layer1 in range(len(word)):
        start = "abandon"
        phrase1 = f"minor zone pool {word[layer1]} remain combine {start} claw medal settle grace capable"
        stack.append(phrase1)
        for layer2 in range(len(word)):
            phrase2 = f"minor zone pool {word[layer1]} remain combine {word[layer2]} claw medal settle grace capable"
            stack.append(phrase2)

    for i in range(len(stack)):
        #print(f'{i + 1} | {stack[i]}')
        wallet_path = f"/home/user/.electrum/electrum_wallet/account_{i}.json"
        seed_phrase = stack[i]
        print(seed_phrase)

        command = ["electrum", "restore", "-w", wallet_path, seed_phrase]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            #print(f"Electrum doesn't recognize seed or key index {i+1}")
            continue

        if os.path.exists(f'/home/user/.electrum/electrum_wallet/account_{i}.json'):
            with io.open(wallet_path, 'r') as file:
                data = json.load(file)

            mnemonic = data["keystore"]["seed"]
            master_key = data["keystore"]["xpub"]

            if _key_ == master_key:
                with open("/home/user/.electrum/ビットコイン会った.txt", "a") as f:
                    f.write(f"{i + 1} | {mnemonic}\n")
                    f.write(f"{i + 1} | {master_key}\n\n")


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Scanning", font="big")
    print(result)
    main()
