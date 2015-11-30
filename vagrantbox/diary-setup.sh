#!/usr/bin/env bash
set -x
# make user
sudo useradd ctf_hacker_diary
sudo mkdir -p /opt/ctf/hacker_diary/{rw,ro,www}

mkdir build
cd build
tar -xzf ../hacker_diary.tgz

# copy service files
sudo cp -a service/rw/* /opt/ctf/hacker_diary/rw
sudo cp -a service/www/* /opt/ctf/hacker_diary/www
sudo cp -a service/ro/* /opt/ctf/hacker_diary/ro

# set ownership and permissions
sudo chown -R root:root /opt
sudo chown -R ctf_hacker_diary:ctf_hacker_diary /opt/ctf/hacker_diary

sudo chmod -R 755 /opt/ctf/
sudo chmod -R 750 /opt/ctf/*/{ro,www}
sudo chmod -R 770 /opt/ctf/*/rw

# copy apache config
sudo cp hacker_diary.conf /etc/apache2/sites-enabled/hacker_diary.conf

#copy xinetd config
sudo cp hacker_diary.xinetd /etc/xinetd.d/hacker_diary.xinetd
sudo echo 'hacker_diary.xinetd 9800/tcp' >>/etc/services
sudo cp wrapper.sh /opt/ctf/hacker_diary/ro/wrapper.sh
sudo service xinetd restart

# install required debian packages
sudo apt-get install -y python3-pip libapache2-mod-wsgi build-essential libssl-dev libffi-dev python3-dev

# switch to run directory
cd /opt/ctf/hacker_diary

# install required pip packages locally
#sudo pip3 install -t /opt/ctf/hacker_diary/.local django djangorestframework cryptography

# run postinstall
cd ro
sudo -u ctf_hacker_diary ./postinst



