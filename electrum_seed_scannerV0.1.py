#!/usr/bin/env python3

import io
import json
import BIP39
import os.path
import pyfiglet
import subprocess


def brute_force():
    wordlist = BIP39.WORDLIST
    return (f"minor zone pool {a} remain combine {b} claw medal settle grace capable"
            for a in wordlist
            for b in wordlist)

def main():
    key = "xpub661MyMwAqRbcH29GtXQXpxfecjcZ3mFNWQ1WhsTRCGSVio9DXDnoufPHRYuukscD9sVD7u4W71VV2EtoLm77xmCRdMpgFoiaQ3MDeiHA33G"
    restore_dir = "/home/user/.electrum/electrum_wallet"
    congratulations_file = "/home/user/.electrum/test1.txt"

    for i, phrase in enumerate(brute_force()):
        #print(f"{i+1} | {phrase}")
        wallet_path = os.path.join(restore_dir, f"account_{i}.json")
        result = subprocess.run(["electrum", "restore", "-w", wallet_path, phrase],
                                capture_output=True, text=True)

        if result.returncode != 0:
            continue

        restore_path = os.path.join(restore_dir, f"account_{i}.json")
        with io.open(restore_path) as f:
            data = json.load(f)

        mnemonic = data["keystore"]["seed"]
        master_key = data["keystore"]["xpub"]

        if key == master_key:
            with io.open(congratulations_file, "a") as f:
                f.write(f"{i + 1} | {mnemonic}\n")
                f.write(f"{i + 1} | {master_key}\n\n")
            print(f"Process finished.. found matching key is now")
            break


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Scanning", font="slant")
    print(result)
    main()
