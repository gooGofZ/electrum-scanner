#!/usr/bin/env python3

import io
import json
import BIP39
import os.path
import pyfiglet
import subprocess

def main():
    key_target = "xpub661MyMwAqRbcH29GtXQXpxfecjcZ3mFNWQ1WhsTRCGSVio9DXDnoufPHRYuukscD9sVD7u4W71VV2EtoLm77xmCRdMpgFoiaQ3MDeiHA33G"

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

        command = ["electrum", "restore", "-w", wallet_path, seed_phrase]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            continue

        if os.path.exists(f'/home/user/.electrum/electrum_wallet/account_{i}.json'):
            with io.open(wallet_path, 'r') as file:
                data = json.load(file)

            mnemonic = data["keystore"]["seed"]
            master_key = data["keystore"]["xpub"]

            if key_target == master_key:
                with io.open("/home/user/.electrum/test2.txt", "a") as f:
                    f.write(f"{i + 1} | {mnemonic}\n")
                    f.write(f"{i + 1} | {master_key}\n\n")
                print(f"Process finished.. found matching key is now")
                break


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Scanning", font="slant")
    print(result)
    main()