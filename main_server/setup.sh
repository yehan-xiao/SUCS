#!/bin/sh
easy_install web.py

apt-get install libmysqlclient-dev python-dev
pip install pip --upgrade
apt-get build-dep python-mysqldb
pip install MySQL-python

pip install googlemaps

