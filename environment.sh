#!/bin/bash

sudo apt update
sudo apt install docker.io
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo apt install git
sudo apt install make
sudo apt-get install openjdk-8-jre
