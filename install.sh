#!/bin/bash

### Install script for CCA Folder Processor in Bitcurator

# Make /usr/share/cca-folderprocessor if doesn't already exist
if [ ! -d /usr/share/cca-folderprocessor ]; then
  sudo mkdir /usr/share/cca-folderprocessor
fi

# Move files into /usr/share/cca-folderprocessor
sudo mv main.py /usr/share/cca-folderprocessor
sudo mv launch /usr/share/cca-folderprocessor
sudo mv design.py /usr/share/cca-folderprocessor
sudo mv design.ui /usr/share/cca-folderprocessor
sudo mv icon.png /usr/share/cca-folderprocessor
sudo mv LICENSE /usr/share/cca-folderprocessor
sudo mv README.md /usr/share/cca-folderprocessor

# Make "CCA Tools" folder on Desktop if doesn't already exist
if [ ! -d "/home/bcadmin/Desktop/CCA Tools" ]; then
  sudo mkdir "/home/bcadmin/Desktop/CCA Tools"
fi

# Create launch.desktop file
sudo touch '/home/bcadmin/Desktop/CCA Tools/Folder Processor.desktop'
echo '[Desktop Entry]' | sudo tee --append '/home/bcadmin/Desktop/CCA Tools/Folder Processor.desktop'
echo 'Type=Application' | sudo tee --append '/home/bcadmin/Desktop/CCA Tools/Folder Processor.desktop'
echo 'Name=Folder Processor' | sudo tee --append '/home/bcadmin/Desktop/CCA Tools/Folder Processor.desktop'
echo 'Exec=/usr/share/cca-folderprocessor/launch' | sudo tee --append '/home/bcadmin/Desktop/CCA Tools/Folder Processor.desktop'
echo 'Icon=/usr/share/cca-folderprocessor/icon.png' | sudo tee --append '/home/bcadmin/Desktop/CCA Tools/Folder Processor.desktop'

# Change permissions, ownership for CCA Tools
sudo chown -R bcadmin:bcadmin '/home/bcadmin/Desktop/CCA Tools'
sudo chown -R bcadmin:bcadmin '/usr/share/cca-folderprocessor'
sudo find '/home/bcadmin/Desktop/CCA Tools' -type d -exec chmod 755 {} \;
sudo find '/home/bcadmin/Desktop/CCA Tools' -type f -exec chmod 644 {} \;

# Make files executable
sudo chmod u+x '/home/bcadmin/Desktop/CCA Tools/Folder Processor.desktop'
sudo chmod u+x /usr/share/cca-folderprocessor/launch
