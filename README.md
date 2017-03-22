# CCA Folder Processor  

Tool for automated processing of directories in Bitcurator.  

**NOTE: This tool is in dev and should not be considered production-ready without testing**

CCA Folder Processor creates Archivematica-ready SIPs from directories on a local filesystem, piece of external media, or network shares, and generates a pre-populated description spreadsheet containing information such as start and end dates, extents, and a scope and content note for each created SIP.

The GUI offers a checkbox interface to select which directories should be turned into SIPs.

CCA Folder Processor creates an md5deep-generated checksum.md5 manifest saved in each SIP's metadata directory (according to Archivematica packaging ventions) as default behavior. To create each SIP as a bag instead, select that option from the GUI interface. Folder Processor can optionally also run a PII scan of each SIP using bulk_extractor as part of the Brunnhilde characterization step of SIP creation and description. Bulk_extractor results are saved to metadata/submissionDocumentation, in the Brunnhilde report output folder.  

### Installation  

This utility is designed for easy use in Bitcurator, and in v1.8.0+ requires installation of only [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download): 
`sudo apt-get install python-qt4`  

Alternatively, install all of the CCA Tools (and PyQT4) using the install script in the [CCA Tools repo](https://github.com/timothyryanwalsh/cca-tools).  
