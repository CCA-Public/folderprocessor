# Folder Processor  

Tool for automated processing of directories in BitCurator.  

Version: 1.0.0

CCA Folder Processor creates Archivematica-ready SIPs from directories on a local filesystem, piece of external media, or network shares, and generates a pre-populated description spreadsheet containing information such as start and end dates, extents, and a scope and content note for each created SIP.

The GUI offers a checkbox interface to select which directories should be turned into SIPs.

CCA Folder Processor creates an md5deep-generated checksum.md5 manifest saved in each SIP's metadata directory (according to Archivematica packaging ventions) as default behavior. To create each SIP as a bag instead, select that option from the GUI interface. Folder Processor can optionally also run a PII scan of each SIP using bulk_extractor as part of the Brunnhilde characterization step of SIP creation and description. Bulk_extractor results are saved to metadata/submissionDocumentation, in the Brunnhilde report output folder.  

## Installation

This utility is designed for easy use in BitCurator v1.8.0+. It requires Python 3 and PyQt5.

### Install as part of CCA Tools  

Install all of the CCA Tools together using the installation script in the [CCA Tools repo](https://github.com/CCA-Public/cca-tools).  

### Install as a separate utlity
* Install [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download):  
`sudo pip3 install pyqt5`  
* Clone this repo to your local machine.  
* Run the install script with sudo privileges:  
`chmod u+x install.sh`  
`sudo ./install.sh`

### PyQt4 version

Please note that Folder Processor v1.0.0 uses PyQt5. Installation of PyQt5 may cause issues with existing PyQt4 programs in BitCurator. For the a PyQt4 version of Folder Processor that will not affect the functionality of other tools, see the commit [efc3cee](https://github.com/CCA-Public/folderprocessor/tree/efc3cee46dbed05727c8c461232df7318a12c46d).
