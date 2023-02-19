#!/bin/bash

### Install script for CCA Folder Processor in Bitcurator

# Update submodules
git submodule update --init --recursive

# Make /usr/share/ccatools if doesn't already exist
if [ ! -d /usr/share/ccatools ]; then
  sudo mkdir /usr/share/ccatools
fi

# Delete /usr/share directory for Folder Processor if it already exists
if [ -d /usr/share/ccatools/folderprocessor ]; then
  sudo rm -rf /usr/share/ccatools/folderprocessor
fi

# Make /usr/share directory for Folder Processor
sudo mkdir /usr/share/ccatools/folderprocessor

# Move files into /usr/share/ccatools/folderprocessor
sudo cp main.py /usr/share/ccatools/folderprocessor
sudo cp launch /usr/share/ccatools/folderprocessor
sudo cp design.py /usr/share/ccatools/folderprocessor
sudo cp design.ui /usr/share/ccatools/folderprocessor
sudo cp icon.png /usr/share/ccatools/folderprocessor
sudo cp LICENSE /usr/share/ccatools/folderprocessor
sudo cp README.md /usr/share/ccatools/folderprocessor
sudo cp deps/dfxml/python/dfxml.py /usr/share/ccatools/folderprocessor
sudo cp deps/dfxml/python/Objects.py /usr/share/ccatools/folderprocessor
sudo cp deps/dfxml/python/walk_to_dfxml.py /usr/share/ccatools/folderprocessor

sudo cp deps/dfxml/python/dfxml.py .
sudo cp deps/dfxml/python/Objects.py .
sudo cp deps/dfxml/python/walk_to_dfxml.py .
