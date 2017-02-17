# Installation Instructions

Note: these instructions assume you're installing Folder Processor on a fresh install of [BitCurator](https://wiki.bitcurator.net/index.php?title=Main_Page) VM v1.7.102.  

### Prepping to Install:

##### 1. Install an updated version of [SIP](https://riverbankcomputing.com/software/sip/intro)

You can try `pip install SIP` or `pip3 install SIP`, but if those are out of date (you need at least SIP 4.19), you will need to...

* Visit <https://riverbankcomputing.com/software/sip/download>. 
* Copy the download link for the Linux source tar.gz
* `wget <copied link>`
* `tar -xzvf <filename>`
* `cd sip-4.19` 
* `python configure.py`
* `make`
* `make install` (may have to do as sudo)

##### 2. Install [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/installation.html) (if you plan on using the GUI)

First, install Qt4: `sudo apt-get install qt4-default`
Then, install PyQt4... 
* Visit <https://riverbankcomputing.com/software/pyqt/download>
* Copy the download link for the Linux source tar.gz
* `wget <copied link>`
* `tar -xzvf <filename>`
* `cd PyQt4_gpl_x11-4.12`
* `python configure-ng.py`
* `make`
* `make install` (may have to do as sudo)
	
##### 3. Install [brunnhilde](https://github.com/timothyryanwalsh/brunnhilde) 
Brunnhilde generates aggregate reports of files in a directory or disk image based on input from Siegfried. Disk Image Processor will run without it, but the reporting capacity will be limited. 
* Get [Siegfried](https://github.com/richardlehane/siegfried/wiki/Getting-started) *(not going to lie, this might be a bit bumpy, but it should work)*
```
wget -qO - https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
echo "deb http://dl.bintray.com/siegfried/debian wheezy main" | sudo tee -a /etc/apt/sources.list
sudo apt-get update && sudo apt-get install siegfried
```

* Install brunnhilde `pip install brunnhilde`  
	
### Installing:

* ```sudo bash install.sh```
Thanks, install script :-)


### Running CCA Folder Processor:  

##### GUI:
* Navigate to the Desktop -> CCA Tools folder
* Click the Folder Processor
* OR `python /usr/share/cca-folderprocessor/main.py`

##### CL:
The underlying script is `folderprocessor.py`. Default behavior is to create a SIP of this source. To create SIPs for each immediate child directory instead, pass the "-c" or "--children" argument.  

Will create metadata/checksum.md5 file saved in metadata directory by default. To create bags instead, pass the "-b" or "--bagfiles" argument.  

To have Brunnhilde also complete a PII scan using bulk_extractor, pass the "-p" or "-piiscan" argument.  

A command to create bagged SIPs for each immediate child directory of source would be:  
```
python folderprocessor.py -bc <source> <destination>
```

