#!/usr/bin/env python3

"""
TODO: โปรแกรมนี้ใช้ทรัพยากรเครื่องเยอะมากใช้ RAM เฉลี่ย 15GB
 - โปรแกรมตัวนี้ผมใช้จริง ในการหาคำที่หายไป และปัจจุบันผมได้เงินคืนมาแล้ว
 - โปรแกรมตัวอื่นที่ทิ้งไว้ คอมพิวเตอร์ทั่วไปบ้านๆ สามารถใช้ได้

 โปรแกรมนี้ทำงานร่วมกับ Electrum
 เราต้องไปติดตั้งและกำหนดค่า rpcport ให้เสร็จก่อนนะครับ
 https://electrum.readthedocs.io/en/latest/jsonrpc.html
 https://electrum.org/#download
"""

import io
import json
import BIP39
import os.path
import pyfiglet
import subprocess
import concurrent.futures


def brute_force():
    wordlist = BIP39.WORDLIST
    return (f"minor zone pool {word4} remain combine {word7} claw medal settle grace capable"
            for word4 in wordlist
            for word7 in wordlist)


def process_seed_phrase(
        seed_phrase: str,  # ชุด Seed
        index:       int,  # นับรอบลูปการวนซ้ำ
        target:      str,  # Master Public Key ของเราที่ต้องการเอาไปเทียบหา
        wallet_path: str   # กำหนดที่อยู่บันทึกไฟล์หากพบว่า Seed ชุดนี้สามารถใช้ได้กับ Electrum
) -> str:
    # electrum restore -w /home/user/.electrum/ビットコイン.txt  "minor zone pool abandon remain combine achieve claw medal settle grace capable"
    send = ["electrum", "restore", "-w", wallet_path, seed_phrase]
    result = subprocess.run(send, capture_output=True, text=True)

    # ถ้าชุด Seed ไม่สามารถใช้ได้กับ Electrum ก็ให้ผ่านไป
    if result.returncode != 0:
        return None

    # อ่านไฟล์จากเส้นทางจาก wallet_path ที่เรากำหนด หากมีไฟล์ account_{index}.json มีอยู่จริงไฟล์ก็จะเปิดออกมาอ่าน
    if os.path.exists(wallet_path):
        with io.open(wallet_path, 'r') as file:
            data = json.load(file)

        # หลังจากเปิดไฟล์และโหลดเนื้อหามาแล้ว, แยกค่าเอาเฉพาะสองค่าที่ต้องการจากข้อมูล JSON
        mnemonic = data["keystore"]["seed"]
        master_key = data["keystore"]["xpub"]

        if target == master_key:
            print(f"found matching key is now \n{wallet_path}")
            # เทียบค่า Master Public Key ที่อ่านจาก JSON ถ้าตรงกับ Master Public Key ของเราและเขียนทันทึกทันที
            with open("/home/user/.electrum/ビットコイン.txt", "a") as f:

                # เขียนบันทึก Seed
                f.write(f"{index + 1} | {mnemonic}\n")

                # เขียนบันทึก Master Public Key
                f.write(f"{index + 1} | {master_key}\n\n")

            return "break"


def main():
    target = "xpub661MyMwAqRbcFqPrfnJyBZJhFgjo83KvuGdZciaW5zCJVgmbmAJDsjmJGoKguZbQVezhTrJCEU5YSnoyiEysF6Uiwdxgz3WqnC87eHJGvzQ"
    # target = "zpub6nhhoBvkc6pNgU3JPwobardNLniafeTGnBkxrw8XLv3DeB24W2ycBD68dNciURmdUdqkbggGRCsSNCHg6UJCnYy4tA1GKMa1ZcRGK4Rpjth"

    thread = 8  # กำหนดจำนวน thread ที่เราต้องการใช้งาน. แก้ไขได้
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        
        # TODO: ถ้าจะนำไปใช้ ต้องแก้ไข้เส้นทางเป็นของตัวเองนะ wallet_path: ตรงนี้เรากำหนดเองว่าต้องการบันทึก account_{i}.json ที่ไหน
        mkdir = '/home/rushmi0/.electrum/electrum_wallet/'
        os.makedirs(mkdir, exist_ok=True)
       
        for index, seed_phrase in enumerate(brute_force()):
            # print(f'{index + 1} | {seed_phrase}')
            wallet_path = mkdir + f"account_{index}.json"
            executor.submit(
                 process_seed_phrase,
                 seed_phrase,
                 index,
                 target,
                 wallet_path
             )
           
            """
            future = executor.submit(
                process_seed_phrase,
                seed_phrase, index,
                target,
                wallet_path + f"/account_{index}.json"
            )

            if future.result() == "break":
                break
            """


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Scanning", font="big")
    print(result)
    main()
