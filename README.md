# cca-folderprocessor
Tool for automated processing of directories in Bitcurator.  

Creates Archivematica-ready SIPs from folders on local filesystem, external media,
and/or network shares, as well as a pre-populated description spreadsheet.  

User inputs single directory. Default behavior is to create a SIP of this source. 
To create SIPs for each immediate child directory instead, pass the "-c" or 
"--children" argument.  

Will create metadata/checksum.md5 file saved in metadata directory by default. 
To create bags instead, pass the "-b" or "--bagfiles" argument.  

To have Brunnhilde also complete a PII scan using bulk_extractor, pass the
"-p" or "-piiscan" argument.
