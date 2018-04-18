#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CCA Folder Processor

Tim Walsh 2017
MIT License
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import csv
import datetime
import os
import shutil
import subprocess
import sys
from time import localtime, strftime

import design

#import Objects.py from python dfxml tools
sys.path.append('/usr/share/dfxml/python')
import Objects

class CheckableDirModel(QDirModel):
    # class to put checkbox on the folders
    dataChanged = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self, parent=None):
        QDirModel.__init__(self, None)
        self.checks = {}

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.CheckStateRole:
            return QDirModel.data(self, index, role)
        else:
            if index.column() == 0:
                return self.checkState(index)

    def flags(self, index):
        return QDirModel.flags(self, index) | Qt.ItemIsUserCheckable

    def checkState(self, index):
        if index in self.checks:
            return self.checks[index]
        else:
            return Qt.Unchecked

    def setData(self, index, value, role):
        if (role == Qt.CheckStateRole and index.column() == 0):
            self.checks[index] = value
            self.dataChanged.emit(index, index)
            return True 

        return QDirModel.setData(self, index, value, role)

class SIPThread(QThread):
    increment_progress_bar = pyqtSignal('QString')

    def __init__(self, dirs_to_process, destination, bagfiles, piiscan, output_dir):
        QThread.__init__(self)
        self.dirs_to_process = dirs_to_process
        self.destination = destination
        self.bagfiles = bagfiles
        self.piiscan = piiscan
        self.output_dir = output_dir

    def __del__(self):
        self.wait()

    def create_sip(self, source, destination, bagfiles, piiscan):
        
        # set paths and create dirs
        basename = os.path.basename(os.path.abspath(source))
        sip_dir = os.path.join(destination, basename)
        object_dir = os.path.join(sip_dir, 'objects')
        original_dir = os.path.join(object_dir, basename)
        metadata_dir = os.path.join(sip_dir, 'metadata')
        subdoc_dir = os.path.join(metadata_dir, 'submissionDocumentation')
        
        for newfolder in sip_dir, object_dir, metadata_dir, subdoc_dir:
            os.makedirs(newfolder)

        # copy files
        try:
            shutil.copytree(source, original_dir, symlinks=False, ignore=None)
        except:
            print("WARNING: Error copying files from " + source + " to " + original_dir) #TODO improve error handling

        # run brunnhilde and write to submissionDocumentation directory
        files_abs = os.path.abspath(object_dir)

        if piiscan == True: # brunnhilde with bulk_extractor
            subprocess.call("brunnhilde.py -zbw '%s' '%s' brunnhilde" % (files_abs, subdoc_dir), shell=True)
        else: # brunnhilde without bulk_extractor
            subprocess.call("brunnhilde.py -zw '%s' '%s' brunnhilde" % (files_abs, subdoc_dir), shell=True)

        # create dfxml and write to submissionDocumentation
        subprocess.call("cd '%s' && python3 /usr/share/dfxml/python/walk_to_dfxml.py > '%s'" % (object_dir, os.path.join(subdoc_dir, 'dfxml.xml')), shell=True)

        # write checksums
        if bagfiles == True: # bag entire SIP
            subprocess.call("bagit.py --processes 4 '%s'" % sip_dir, shell=True)
        else: # write metadata/checksum.md5
            subprocess.call("cd '%s' && md5deep -rl ../objects > checksum.md5" % metadata_dir, shell=True)

        # modify file permissions
        subprocess.call("find '%s' -type d -exec chmod 755 {} \;" % sip_dir, shell=True)
        subprocess.call("find '%s' -type f -exec chmod 644 {} \;" % sip_dir, shell=True)

    def create_spreadsheet(self, output_dir, sips, bagfiles):

        spreadsheet_path = os.path.join(output_dir, 'description.csv')
        # open description spreadsheet
        try:
            spreadsheet = open(spreadsheet_path, 'w')
            writer = csv.writer(spreadsheet, quoting=csv.QUOTE_NONNUMERIC)
            header_list = ['Parent ID', 'Identifier', 'Title', 'Archive Creator', 'Date expression', 'Date start', 'Date end', 
                            'Level of description', 'Extent and medium', 'Scope and content', 'Arrangement (optional)', 'Accession number', 
                            'Appraisal, destruction, and scheduling information (optional)', 'Name access points (optional)', 
                            'Geographic access points (optional)', 'Conditions governing access (optional)', 'Conditions governing reproduction (optional)', 
                            'Language of material (optional)', 'Physical characteristics & technical requirements affecting use (optional)', 
                            'Finding aids (optional)', 'Related units of description (optional)', 'Archival history (optional)', 
                            'Immediate source of acquisition or transfer (optional)', "Archivists' note (optional)", 'General note (optional)', 
                            'Description status']
            writer.writerow(header_list)
        except:
            sys.exit('There was an error creating the processing spreadsheet.')

        # close description spreadsheet
        spreadsheet.close()

        # add info to description spreadsheet
        for item in os.listdir(sips):

            # get abspath of entry
            item = os.path.abspath(os.path.join(sips, item))
            
            # test if entry if directory
            if os.path.isdir(item):
            
                if bagfiles == True:
                    subprocess.call("python3 /usr/share/ccatools/folderprocessor/create_spreadsheet.py -b '%s' '%s'" % (item, spreadsheet_path), shell=True)
                else:
                    subprocess.call("python3 /usr/share/ccatools/folderprocessor/create_spreadsheet.py '%s' '%s'" % (item, spreadsheet_path), shell=True)


    def run(self):
        for dir_to_process in self.dirs_to_process:
            self.create_sip(dir_to_process, self.destination, self.bagfiles, self.piiscan)
            self.increment_progress_bar.emit(dir_to_process)
            self.create_spreadsheet(self.output_dir, self.destination, self.bagfiles)


class ProcessorApp(QMainWindow, design.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ProcessorApp, self).__init__(parent)
        self.setupUi(self)

        # build browse functionality buttons
        self.sourceBtn.clicked.connect(self.browse_source)
        self.destinationBtn.clicked.connect(self.browse_dest)

        # build start functionality
        self.processBtn.clicked.connect(self.start_processing)

        # about menu functionality
        self.actionAbout.triggered.connect(self.about_dialog)

        # set progress bar to 0
        self.progressBar.setValue(0)

    def about_dialog(self):
        QMessageBox.information(self, "About", 
            "Folder Processor v1.0.0\nCanadian Centre for Architecture\nDeveloper: Tim Walsh\n2018\nMIT License\nhttps://github.com/CCA-Public/cca-folderprocessor")

    def browse_source(self):
        source = QFileDialog.getExistingDirectory(self, "Select folder")

        if source: # if user didn't pick directory don't continue
            self.model = CheckableDirModel()
            self.treeView.setModel(self.model)
            self.treeView.setSortingEnabled(True)
            self.treeView.setRootIndex(self.model.index(source))

    def browse_dest(self):
        self.destination.clear() # clear directory source text
        directory = QFileDialog.getExistingDirectory(self, "Select folder")

        if directory: # if user didn't pick directory don't continue
            self.destination.setText(directory)

    def increment_progress_bar(self, dir_to_process):
        # TODO something with name of sip processed?
        self.progressBar.setValue(self.progressBar.value()+1)

    def done(self):
        self.cancelBtn.setEnabled(False)
        self.processBtn.setEnabled(True)
        self.progressBar.setValue(self.progressBar.value()+1)
        QMessageBox.information(self, "Done!", "Process complete.")
        self.status.setText('Completed')
        self.progressBar.setValue(0)

    def start_processing(self):
        # acknowledge process has started
        self.status.setText('Processing. Please be patient.')

        # create list of paths for checked folders
        dirs_to_process = []
        for index,value in self.model.checks.items():
            if value != 0:
                if os.path.isdir(self.model.filePath(index)):
                    dirs_to_process.append(self.model.filePath(index))

        # prepare progress bar
        self.progressBar.setMaximum(len(dirs_to_process)+1)
        self.progressBar.setValue(0)

        # create output directories
        destination = str(self.destination.text())

        if not os.path.exists(destination):
            os.makedirs(destination)
        sips = os.path.join(destination, 'SIPs')
        os.makedirs(sips)

        # handle argument checkboxes
        bagfiles = False
        piiscan = False
        if self.bagSIPs.isChecked():
            bagfiles = True
        if self.bulkExt.isChecked():
            piiscan = True

        # create SIP for each item in list and spreadsheet describing all created SIPs
        self.get_thread = SIPThread(dirs_to_process, sips, bagfiles, piiscan, destination)
        self.get_thread.increment_progress_bar['QString'].connect(self.increment_progress_bar)
        self.get_thread.finished.connect(self.done)
        self.get_thread.start()
        self.cancelBtn.setEnabled(True)
        self.cancelBtn.clicked.connect(self.get_thread.terminate)
        self.processBtn.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    form = ProcessorApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
