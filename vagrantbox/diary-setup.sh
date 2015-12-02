#!/usr/bin/env bash
# make user
sudo useradd ctf_hacker_diary -d /opt/ctf/hacker_diary
sudo mkdir -p /opt/ctf/hacker_diary/{rw,ro,www}

cd /vagrant
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

cd ..
# copy apache config
sudo cp hacker_diary.conf /etc/apache2/sites-enabled/hacker_diary.conf

#copy xinetd config
sudo cp hacker_diary.xinetd /etc/xinetd.d/hacker_diary

sudo echo 'hacker_diary 9800/tcp' >>/etc/services
sudo cp wrapper.sh /opt/ctf/hacker_diary/ro/wrapper.sh
sudo service xinetd restart

# install required debian packages
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev

# switch to run directory
cd /opt/ctf/hacker_diary

# install required pip packages locally
sudo -H -u ctf_hacker_diary pip install --user django==1.8 djangorestframework cryptography

# run postinstall
cd rw
sudo -H -u ctf_hacker_diary ../ro/postinst



