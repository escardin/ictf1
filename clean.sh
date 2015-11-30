#!/usr/bin/env bash

find ./ -name *.pyc -delete

rm vagrantbox/{service,src,scripts,hacker_diary.tgz}
rm -rf build

rm -rf **.pyc