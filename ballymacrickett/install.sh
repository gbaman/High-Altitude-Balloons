#!/usr/bin/env bash

sudo apt update
sudo apt install python3-pytrack

sudo pip3 install -r requirements.txt

cp tracker.service /lib/systemd/system/tracker.service -f