#!/usr/bin/env bash

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get -y install curl apache2 libapache2-mod-php5 gdebi xinetd qemu-user-static \
    qemu-user python-pip sqlite3 libsqlite3-dev libapache2-mpm-itk apache2-mpm-itk apache2-bin
sudo apt-get -y install libapache2-mpm-itk apache2-mpm-itk
echo $PWD

./diary-setup.sh