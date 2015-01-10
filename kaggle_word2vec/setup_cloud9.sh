#!/bin/bash

sudo apt-get install -y python-pip python-pandas

sudo pip install BeautifulSoup4

### building pandas sucks up memory, create a swap file if there are problems
# sudo dd if=/dev/zero of=/swapfile bs=1024 count=256k
# sudo chown root:root /swapfile 
# sudo chmod 0600 /swapfile
# sudo mkswap /swapfile
# sudo swapon /swapfile

sudo pip install --upgrade sqlalchemy
sudo pip install --upgrade numpy
sudo pip install --upgrade pandas 
sudo pip install --upgrade blaze