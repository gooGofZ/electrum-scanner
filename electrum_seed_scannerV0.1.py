#!/usr/bin/env python3

import io
import json
import os
import subprocess
import BIP39
import pyfiglet

def brute_force():
    wordlist = BIP39.WORDLIST
    return (f"minor zone pool {a} remain combine {b} claw medal settle grace capable"
            for a in wordlist
            for b in wordlist)

def main():
    key = "zpub6nhhoBvkc6pNgU3JPwobardNLniafeTGnBkxrw8XLv3DeB24W2ycBD68dNciURmdUdqkbggGRCsSNCHg6UJCnYy4tA1GKMa1ZcRGK4Rpjth"
    restore_dir = "/home/rushmi0/.electrum/raw_data"
    congratulations_file = "/home/rushmi0/.electrum/ビットコイン会った.txt"

    for i, phrase in enumerate(brute_force()):
        #print(f"{i+1} | {phrase}")

        wallet_path = os.path.join(restore_dir, f"restore_{i}.json")

        result = subprocess.run(["electrum", "restore", "-w", wallet_path, phrase],
                                capture_output=True, text=True)

        if result.returncode != 0:
            #print(f"Electrum doesn't recognize seed or key index {i+1}")
            continue

        restore_path = os.path.join(restore_dir, f"restore_{i}.json")
        with open(restore_path) as f:
            data = json.load(f)

        mnemonic, master_key = ({data["keystore"][k] for k in ["seed", "xpub"]})

        if key == master_key:
            with open(congratulations_file, "a") as f:
                f.write(f"{i + 1} | {mnemonic}\n")
                f.write(f"{i + 1} | {master_key}\n\n")


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Scanning", font="slant")
    print(result)
    main()