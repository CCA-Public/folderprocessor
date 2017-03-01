# CCA Folder Processor  

## Version 1.0  

Tool for automated processing of directories in Bitcurator.  

CCA Folder Processor creates Archivematica-ready SIPs from directories on a local filesystem, piece of external media, or network shares, and generates a pre-populated description spreadsheet containing information such as start and end dates, extents, and a scope and content note for each created SIP.

The GUI offers a checkbox interface to select which directories should be turned into SIPs.

CCA Folder Processor creates an md5deep-generated md5 checksum.md5 manifest saved in a metadata directory (according to Archivematica packaging ventions) as default behavior. To create each SIP as a bag instead, select that option from the GUI interface. Folder Processor can optionally also run a PII scan of eahc SIP using bulk_extractor as part of the Brunnhilde characterization step of SIP creation and description. Bulk_extractor results are saved to metadata/submissionDocumentation.  
