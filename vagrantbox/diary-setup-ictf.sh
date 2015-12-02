#!/usr/bin/env bash
cd /vagrant
mkdir build
cd build
tar -xzf ../hacker_diary.tgz
cp -a service/* /opt/ctf/
mv /opt/ctf/service /opt/ctf/hacker_diary 
useradd -d /opt/ctf/hacker_diary -s /bin/bash --user-group ctf_hacker_diary 
echo >/etc/sudoers.d/sudo_for_ctf_hacker_diary ctf ALL= (ctf_hacker_diary:ctf_hacker_diary) NOPASSWD: ALL
chown -R ctf:ctf_hacker_diary /opt/ctf/hacker_diary 
chmod -R 770 /opt/ctf/hacker_diary 
apt-get install -q -y  build-essential libssl-dev libffi-dev python-dev 
sudo -H -u ctf_hacker_diary mkdir /opt/ctf/hacker_diary/.local 
sudo -H -u ctf_hacker_diary pip install --user django djangorestframework cryptography 
chown -R ctf:ctf_hacker_diary /opt/ctf/hacker_diary/.local 
chmod -R 770 /opt/ctf/hacker_diary/.local 
chmod -R g-w /opt/ctf/hacker_diary/.local 
chown root:root /opt/ctf/hacker_diary 
chmod 755 /opt/ctf/hacker_diary 
chmod -R g-w /opt/ctf/hacker_diary/ro 
echo >/etc/xinetd.d/hacker_diary service hacker_diary\n{\n    socket_type = stream\n    protocol    = tcp\n    wait        = no\n    user        = ctf_hacker_diary\n    bind        = 0.0.0.0\n    server      = /opt/ctf/hacker_diary/ro/wrapper.sh\n    port        = 31337\n    type        = UNLISTED\n    instances   = 50\n}\n
echo >/opt/ctf/hacker_diary/ro/wrapper.sh #!/bin/bash\ncd /opt/ctf/hacker_diary/rw\n./../ro/hacker_diary 2>/dev/null\n
chmod +x /opt/ctf/hacker_diary/ro/wrapper.sh 
sudo -u ctf_hacker_diary bash -c "cd /opt/ctf/hacker_diary/rw; ../ro/postinst" 
rm /opt/ctf/hacker_diary/ro/postinst


