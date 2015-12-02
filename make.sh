#!/usr/bin/env bash

mkdir -p build/{src,scripts,service/{ro,rw}}
#info file
cp info.yaml build

#setup src folder
cp -a -t build/src diary ictf1 scripts vagrantbox info.yaml make.sh manage.py postinst setup.py

#setup scripts folder
cp -a -t build/scripts scripts/*

#setup service/ro folder
cp -a -t build/service/ro postinst setup.py manage.py diary ictf1 hacker_diary

#setup service/www folder
#cp -a -t build/service/www postinst setup.py manage.py diary ictf1

#setup service/rw folder
cd build/service/ro
python setup.py
python manage.py migrate
cd ../../..

#tarball it all
cd build
tar -czf hacker_diary.tgz *
cp hacker_diary.tgz ../vagrantbox