#!/usr/bin/env bash

sudo apt update
sudo apt install python3-pytrack -y

sudo pip3 install -r requirements.txt

sudo cp tracker.service /lib/systemd/system/tracker.service -f

sudo systemctl enable tracker.service
sudo service tracker start