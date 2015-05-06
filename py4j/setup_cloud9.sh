#!/bin/bash

sudo apt-get install -y scala

sudo bash -c "echo deb ssh://ddboline@ddbolineathome.mooo.com/var/www/html/deb/trusty/pip_py2deb ./ > /etc/apt/sources.list.d/py2deb2.list"
sudo apt-get update

sudo apt-get install -y --force-yes py4j
