#!/usr/bin/env python3

"""
TODO: โปรแกรมนี้ใช้ทรัพยากรเครื่องเยอะมาก CPU วิ่ง 100% ทุกเธรด!!! (กำหนดจำนวนเธรดได้)  และใช้ RAM เฉลี่ย 16GB
 - โปรแกรมตัวนี้ผมใช้จริง ในการหาคำที่หายไป และปัจจุบันผมได้เงินคืนมาแล้ว
 - โปรแกรมตัวอื่นที่ทิ้งไว้ คอมพิวเตอร์บ้านๆ สามารถใช้ได้

 โปรแกรมนี้ทำงานร่วมกับ Electrum
 เราต้องไปติดตั้งและกำหนดค่า rpcport ให้เสร็จก่อนนะครับ
"""


import io
import json
import BIP39
import os.path
import pyfiglet
import subprocess
import concurrent.futures


def brute_force():
    word = BIP39.WORDLIST
    start = "abandon"
    for layer1 in range(len(word)):
        phrase1 = f"minor zone pool {word[layer1]} remain combine {start} claw medal settle grace capable"
        yield phrase1
        for layer2 in range(len(word)):
            phrase2 = f"minor zone pool {word[layer1]} remain combine {word[layer2]} claw medal settle grace capable"
            yield phrase2


def process_seed_phrase(
                         seed_phrase,    # ชุด Seed
                         index,          # นับรอบลูปการวนซ้ำ
                         target,         # Master Public Key ของเราที่ต้องการเอาไปเทียบหา
                         wallet_path     # กำหนดที่อยู่ไฟล์หากพบว่า Seed ชุดนี้สามารถใช้ได้กับ Electrum
                        ):

 
    # electrum restore -w /home/user/.electrum/ビットコインに会った.txt  "minor zone pool abandon remain combine achieve claw medal settle grace capable"
    command = ["electrum", "restore", "-w", wallet_path, seed_phrase]
    result = subprocess.run(command, capture_output=True, text=True)

    # ถ้าชุด Seed ไม่สามารถใช้ได้กับ Electrum ก็ให้ผ่านไป เพื่อให้โปรแกรมยังคงทำงานต่อไป
    if result.returncode != 0:
        return # ป้องกันโปรแกรมไม่ให้รันโค้ดต่อไปได้

    # อ่านไฟล์จากเส้นทางจาก wallet_path ที่เรากำหนด หากมีไฟล์ account_{i}.json อยู่จริงไฟล์นั้นจะเปิดออกมาอ่าน
    if os.path.exists(wallet_path):
        with io.open(wallet_path, 'r') as file:
            data = json.load(file)

        # หลังจากเปิดไฟล์และโหลดเนื้อหามาแล้ว, แยกค่าเอาเฉพาะสองค่าที่ต้องการจากข้อมูล JSON ที่โหลด และกำหนดให้กับตัวแปร
        mnemonic = data["keystore"]["seed"]
        master_key = data["keystore"]["xpub"]

        if target == master_key:

            # ถ้าค่า Master Public Key ที่จาก JSON ตรงกับ Master Public Key ของเรา.. จะเขียนทันทึกทันที
            with io.open("/home/user/.electrum/ビットコインに会った.txt", "a") as f:

                # เขียนบันทึก Seed
                f.write(f"{index + 1} | {mnemonic}\n")

                # เขียนบันทึก Master Public Key
                f.write(f"{index + 1} | {master_key}\n\n")
                
                if target == master_key:
                    print(f"Process finished.. found matching key is now")
                    return "break"


def main():
    target = "zpub6nhhoBvkc6pNgU3JPwobardNLniafeTGnBkxrw8XLv3DeB24W2ycBD68dNciURmdUdqkbggGRCsSNCHg6UJCnYy4tA1GKMa1ZcRGK4Rpjth"

    thread = 8  # กำหนดจำนวน thread ที่เราต้องการใช้งาน. CPU ของผมมี 4 core 8 thread ผมต้องการให้การคำนวณแบบสุดกำลัง ผมจึงใช้ 8 thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        for i, seed_phrase in enumerate(brute_force()):
            # print(f'{i + 1} | {seed_phrase}')
        
            # TODO: ถ้าจะนำไปใช้ ต้องแก้ไข้เส้นทางเป็นของตัวเองนะ wallet_path: ตรงนี้เรากำหนดเองว่าต้องการบันทึก account_{i}.json ที่ไหน
            wallet_path = f"/home/user/.electrum/electrum_wallet/account_{i}.json"
            future = executor.submit(process_seed_phrase, seed_phrase, i, target, wallet_path)

            if future.result() == "break":
                break


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Scanning", font="big")
    print(result)
    main()
