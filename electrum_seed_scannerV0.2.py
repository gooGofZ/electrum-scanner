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
        phrase1 = f"word1 word2 word3 {word[layer1]} word5 word6 {start} word8 word9 word10 word11 word12"
        stack.append(phrase1)
        for layer2 in range(len(word)):
            phrase2 = f"word1 word2 word3 {word[layer1]} word5 word6 {word[layer2]} word8 word9 word10 word11 word12"
            stack.append(phrase2)

    for i in range(len(stack)):
        #print(f'{i + 1} | {stack[i]}')
        wallet_path = f"/home/rushmi0/.electrum/electrum_wallet/account_{i}.json"
        seed_phrase = stack[i]
        print(seed_phrase)

        command = ["electrum", "restore", "-w", wallet_path, seed_phrase]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            #print(f"Electrum doesn't recognize seed or key index {i+1}")
            continue

        if os.path.exists(f'/home/rushmi0/.electrum/electrum_wallet/restore_{i}.json'):
            with io.open(wallet_path, 'r') as file:
                data = json.load(file)

            mnemonic = data["keystore"]["seed"]
            master_key = data["keystore"]["xpub"]

            if _key_ == master_key:
                with open("/home/rushmi0/.electrum/ビットコイン会った.txt", "a") as f:
                    f.write(f"{i + 1} | {mnemonic}\n")
                    f.write(f"{i + 1} | {master_key}\n\n")


if __name__ == "__main__":
    result = pyfiglet.figlet_format("[Mining V2]", font="slant")
    print(result)
    main()
