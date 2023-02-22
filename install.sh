#!/bin/bash

### Install script for CCA Disk Image Processor in Bitcurator 4/Ubuntu 22

git submodule update --init --recursive

if [ ! -d /usr/share/ccatools ]; then
  sudo mkdir /usr/share/ccatools
fi

folderprocessor_dir="/usr/share/ccatools/folderprocessor/"

if [ -d $folderprocessor_dir ]; then
  sudo rm -rf $folderprocessor_dir
fi

sudo mkdir $folderprocessor_dir

sudo cp main.py $folderprocessor_dir
sudo cp launch $folderprocessor_dir
sudo cp design.py $folderprocessor_dir
sudo cp design.ui $folderprocessor_dir
sudo cp icon.png $folderprocessor_dir
sudo cp LICENSE $folderprocessor_dir
sudo cp README.md $folderprocessor_dir
sudo cp deps/dfxml/python/dfxml.py $folderprocessor_dir
sudo cp deps/dfxml/python/Objects.py $folderprocessor_dir
sudo cp deps/dfxml/python/walk_to_dfxml.py $folderprocessor_dir

# Create launch.desktop file
launch_file="/usr/share/applications/FolderProcessor.desktop"

if [ -f $launch_file ]; then
  sudo rm -rf $launch_file
fi

sudo touch $launch_file
echo '[Desktop Entry]' | sudo tee --append $launch_file
echo 'Type=Application' | sudo tee --append $launch_file
echo 'Name=Folder Processor' | sudo tee --append $launch_file
echo 'Exec=/usr/share/ccatools/folderprocessor/launch' | sudo tee --append $launch_file
echo 'Icon=/usr/share/ccatools/folderprocessor/icon.png' | sudo tee --append $launch_file
echo 'Categories=Forensics and Reporting' | sudo tee --append $launch_file

sudo chown -R bcadmin:bcadmin $folderprocessor_dir
sudo chmod u+x /usr/share/ccatools/folderprocessor/launch
