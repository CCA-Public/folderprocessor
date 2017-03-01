# CCA Folder Processor  

## Version 2.0  

Tool for automated processing of directories in Bitcurator.  

Creates Archivematica-ready SIPs from folders on local filesystem, external media, and/or network shares, as well as a pre-populated description spreadsheet.  

User selects folders to create SIPs from by checking appropriate boxes.  

Will create md5deep-generated md5 manifest saved in metadata directory (for reading by Archivematica on transfer) by default. To create bags instead, select that option from the GUI interface.  

Optionally also has Brunnhilde complete a PII scan using bulk_extractor.  