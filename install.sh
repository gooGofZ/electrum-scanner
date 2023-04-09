#!/bin/bash

sudo apt-get install python3-pyqt5 libsecp256k1-0 python3-cryptography -y
sudo apt-get install python3-setuptools python3-pip -y

wget https://download.electrum.org/4.3.4/Electrum-4.3.4.tar.gz
tar -xvf Electrum-4.3.4.tar.gz
python3 -m pip install --user Electrum-4.3.4.tar.gz

electrum setconfig rpcport 7777
electrum setconfig rpcuser VM
electrum setconfig rpcpassword VM123

reboot
