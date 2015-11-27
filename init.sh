#!/bin/bash

apt-get -y install python wget

if [ ! -d download ]; then
  mkdir download
fi
python setup.py
