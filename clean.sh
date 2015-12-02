#!/usr/bin/env bash

find ./ -name *.pyc -delete

rm -rf vagrantbox/{build,hacker_diary.tgz}
rm -rf build

rm -rf **.pyc