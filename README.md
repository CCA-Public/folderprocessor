# CCA Folder Processor  

Tool for automated processing of directories in BitCurator.  

**NOTE: This tool is in dev and should not be considered production-ready without testing**
Version: 0.2.0 (beta)

CCA Folder Processor creates Archivematica-ready SIPs from directories on a local filesystem, piece of external media, or network shares, and generates a pre-populated description spreadsheet containing information such as start and end dates, extents, and a scope and content note for each created SIP.

The GUI offers a checkbox interface to select which directories should be turned into SIPs.

CCA Folder Processor creates an md5deep-generated checksum.md5 manifest saved in each SIP's metadata directory (according to Archivematica packaging ventions) as default behavior. To create each SIP as a bag instead, select that option from the GUI interface. Folder Processor can optionally also run a PII scan of each SIP using bulk_extractor as part of the Brunnhilde characterization step of SIP creation and description. Bulk_extractor results are saved to metadata/submissionDocumentation, in the Brunnhilde report output folder.  

## Installation

This utility is designed for easy use in BitCurator v1.8.0+. It requires Python 2.7 (to run the GUI) and Python 3.4+ (to analyze DFXML), both of which are already included in BitCurator.  

### Install as part of CCA Tools  

Install all of the CCA Tools (and PyQT4) together using the install bash script in the [CCA Tools repo](https://github.com/timothyryanwalsh/cca-tools).  

### Install as a separate utlity
* Install [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download):  
`sudo apt-get install python-qt4`  
* Clone this repo to your local machine.  
* Run the install script with sudo privileges:  
`sudo bash install.sh`  
