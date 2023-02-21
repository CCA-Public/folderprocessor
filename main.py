"""
CCA Folder Processor

(c) Canadian Centre for Architecture
Developed by Tessa Walsh
2017-2023
MIT License
"""
import csv
import datetime
import itertools
import math
import os
import shutil
import subprocess
import sys
from time import localtime, strftime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import design
import Objects


CSV_HEADERS = [
    "Parent ID",
    "Identifier",
    "Title",
    "Archive Creator",
    "Date expression",
    "Date start",
    "Date end",
    "Level of description",
    "Extent and medium",
    "Scope and content",
    "Arrangement (optional)",
    "Accession number",
    "Appraisal, destruction, and scheduling information (optional)",
    "Name access points (optional)",
    "Geographic access points (optional)",
    "Conditions governing access (optional)",
    "Conditions governing reproduction (optional)",
    "Language of material (optional)",
    "Physical characteristics & technical requirements affecting use (optional)",
    "Finding aids (optional)",
    "Related units of description (optional)",
    "Archival history (optional)",
    "Immediate source of acquisition or transfer (optional)",
    "Archivists' note (optional)",
    "General note (optional)",
    "Description status",
]


def convert_size(size):
    """Convert size in bytes to human-readable string."""
    if size == 0:
        return "0 bytes"
    size_name = ("bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p)
    s = str(s)
    s = s.replace(".0", "")
    return "{} {}".format(s, size_name[i])


class CheckableDirModel(QDirModel):
    """Class to put checkbox on the folders."""
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
        if role == Qt.CheckStateRole and index.column() == 0:
            self.checks[index] = value
            self.dataChanged.emit(index, index)
            return True

        return QDirModel.setData(self, index, value, role)


class SIPThread(QThread):
    """QThread used to create SIPs and write descriptive CSV."""
    increment_progress_bar = pyqtSignal("QString")

    def __init__(
        self, dirs_to_process, destination, bag_files, scan_for_pii, output_dir
    ):
        QThread.__init__(self)
        self.dirs_to_process = dirs_to_process
        self.destination = destination
        self.bag_files = bag_files
        self.scan_for_pii = scan_for_pii
        self.output_dir = output_dir

    def __del__(self):
        self.wait()

    def create_sip(self, source, destination, bag_files, scan_for_pii):
        """Create SIP from source directory."""
        basename = os.path.basename(os.path.abspath(source))
        sip_dir = os.path.join(destination, basename)
        object_dir = os.path.join(sip_dir, "objects")
        original_dir = os.path.join(object_dir, basename)
        metadata_dir = os.path.join(sip_dir, "metadata")
        subdoc_dir = os.path.join(metadata_dir, "submissionDocumentation")

        for newfolder in sip_dir, object_dir, metadata_dir, subdoc_dir:
            os.makedirs(newfolder)

        try:
            shutil.copytree(source, original_dir, symlinks=False, ignore=None)
        except shutil.Error as err:
            print(
                "Error copying files from {} to {}: {}".format(
                    source, original_dir, err
                )
            )
            return 1

        # Run Brunnhilde and write results to submissionDocumentation.
        objects_abspath = os.path.abspath(object_dir)
        brunnhilde_cmd = "brunnhilde.py -zw '{}' '{}' brunnhilde".format(
            objects_abspath, subdoc_dir
        )
        if scan_for_pii:
            brunnhilde_cmd = "brunnhilde.py -zbw '{}' '{}' brunnhilde".format(
                objects_abspath, subdoc_dir
            )
        subprocess.call(brunnhilde_cmd, shell=True)

        # Write DFXML to submissionDocumentation
        dfxml_path = os.path.join(subdoc_dir, "dfxml.xml")
        dfxml_cmd = "cd '{}' && python3 /usr/share/ccatools/folderprocessor/walk_to_dfxml.py > '{}'".format(
            object_dir, dfxml_path
        )
        subprocess.call(dfxml_cmd, shell=True)

        # Bag files or write checksum manifest.
        if bag_files:
            # TODO: Multithread bagging via --processes when bug described at
            # https://github.com/LibraryOfCongress/bagit-python/issues/130 is
            # resolved.
            subprocess.call("cd ~ && bagit.py '{}'".format(sip_dir), shell=True)
        else:
            md5deep_cmd = "cd '{}' && md5deep -rl ../objects > checksum.md5".format(
                metadata_dir
            )
            subprocess.call(md5deep_cmd, shell=True)

        # Set file permissions.
        subprocess.call(
            "find '%s' -type d -exec chmod 755 {} \;" % (sip_dir), shell=True
        )
        subprocess.call(
            "find '%s' -type f -exec chmod 644 {} \;" % (sip_dir), shell=True
        )

    def write_description_csv(self, output_dir, sips, bag_files):
        """Write description CSV."""
        csv_path = os.path.join(output_dir, "description.csv")
        with open(csv_path, "w") as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(CSV_HEADERS)
            for item in os.listdir(sips):
                sip_path = os.path.abspath(os.path.join(sips, item))
                if not os.path.isdir(sip_path):
                    continue
                self.write_csv_row(writer, sip_path, bag_files)

    @staticmethod
    def write_csv_row(writer, sip_path, bag_files):
        """Write CSV row for SIP directory."""
        file_count = 0
        total_bytes = 0
        mtimes = []

        # Parse FileObjects in DFXML file.
        dfxml_file = os.path.abspath(
            os.path.join(sip_path, "metadata", "submissionDocumentation", "dfxml.xml")
        )
        if bag_files:
            dfxml_file = os.path.abspath(
                os.path.join(
                    sip_path, "data", "metadata", "submissionDocumentation", "dfxml.xml"
                )
            )
        for (event, obj) in Objects.iterparse(dfxml_file):
            if not isinstance(obj, Objects.FileObject):
                continue
            file_count += 1
            mtime = ""
            if obj.mtime:
                mtime = str(obj.mtime)
            mtimes.append(mtime)
            total_bytes += obj.filesize

        # Build extent statement.
        size_readable = convert_size(total_bytes)
        extent = "EMPTY"
        if file_count == 1:
            extent = "1 digital file ({})".format(size_readable)
        if file_count > 1:
            extent = "{} digital files ({})".format(file_count, size_readable)

        # Build date statement from modified dates.
        date_earliest = "N/A"
        date_latest = "N/A"
        if mtimes:
            date_earliest = min(mtimes)[:10]
            date_latest = max(mtimes)[:10]
        date_statement = "{} - {}".format(date_earliest[:4], date_latest[:4])
        if date_earliest[:4] == date_latest[:4]:
            date_statement = date_earliest[:4]

        # Write scope and content note from information in brunnhilde reports.
        scope_content = ""
        if extent != "EMPTY":
            file_formats = []
            fileformat_csv = os.path.join(
                sip_path,
                "metadata",
                "submissionDocumentation",
                "brunnhilde",
                "csv_reports",
                "formats.csv",
            )
            if bag_files:
                fileformat_csv = os.path.join(
                    sip_path,
                    "data",
                    "metadata",
                    "submissionDocumentation",
                    "brunnhilde",
                    "csv_reports",
                    "formats.csv",
                )
            with open(fileformat_csv, "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in itertools.islice(reader, 5):
                    file_formats.append(row[0])
            file_formats = [format_ or "Unidentified" for format_ in file_formats]
            formats_list = ", ".join(file_formats)
            scope_content = 'Original directory name: "{}". Most common file formats: {}'.format(
                os.path.basename(sip_path), formats_list
            )

        writer.writerow(
            [
                "",
                os.path.basename(sip_path),
                "",
                "",
                date_statement,
                date_earliest,
                date_latest,
                "File",
                extent,
                scope_content,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )

    def run(self):
        """Process directories."""
        for dir_to_process in self.dirs_to_process:
            self.create_sip(
                dir_to_process, self.destination, self.bag_files, self.scan_for_pii
            )
            self.increment_progress_bar.emit(dir_to_process)
            self.write_description_csv(
                self.output_dir, self.destination, self.bag_files
            )


class ProcessorApp(QMainWindow, design.Ui_MainWindow):
    """PyQt application class."""

    def __init__(self, parent=None):
        super(ProcessorApp, self).__init__(parent)
        self.setupUi(self)

        # Connect buttons to their functionality.
        self.sourceBtn.clicked.connect(self.browse_source)
        self.destinationBtn.clicked.connect(self.browse_dest)
        self.processBtn.clicked.connect(self.start_processing)

        # Connect About dialog.
        self.actionAbout.triggered.connect(self.about_dialog)

        self.progressBar.setValue(0)

    def about_dialog(self):
        """Set About dialog."""
        QMessageBox.information(
            self,
            "About",
            "Folder Processor v1.1.0\nCanadian Centre for Architecture\nDeveloper: Tessa Walsh\n2018-2023\nMIT License\nhttps://github.com/CCA-Public/folderprocessor",
        )

    def browse_source(self):
        """Browse and set source directory."""
        source = QFileDialog.getExistingDirectory(self, "Select folder")
        if source:
            self.model = CheckableDirModel()
            self.treeView.setModel(self.model)
            self.treeView.setSortingEnabled(True)
            self.treeView.setRootIndex(self.model.index(source))

    def browse_dest(self):
        """Browse and set destination directory."""
        self.destination.clear()
        directory = QFileDialog.getExistingDirectory(self, "Select folder")
        if directory:
            self.destination.setText(directory)

    def increment_progress_bar(self, dir_to_process):
        """Increment progress bar."""
        self.progressBar.setValue(self.progressBar.value() + 1)

    def done(self):
        """Handle process completion."""
        self.cancelBtn.setEnabled(False)
        self.processBtn.setEnabled(True)
        self.progressBar.setValue(self.progressBar.value() + 1)
        QMessageBox.information(self, "Done!", "Process complete.")
        self.status.setText("Completed")
        self.progressBar.setValue(0)

    def start_processing(self):
        """Handle starting Create SIPs process."""
        self.status.setText("Processing. Please be patient.")

        # Create list of paths for checked folders.
        dirs_to_process = []
        for index, value in self.model.checks.items():
            if value != 0:
                if os.path.isdir(self.model.filePath(index)):
                    dirs_to_process.append(self.model.filePath(index))

        # Prepare progress bar.
        self.progressBar.setMaximum(len(dirs_to_process) + 1)
        self.progressBar.setValue(0)

        # Create output directories.
        destination = str(self.destination.text())
        if not os.path.exists(destination):
            os.makedirs(destination)
        sips = os.path.join(destination, "SIPs")
        os.makedirs(sips)

        # Parse checkboxes.
        bag_files = False
        if self.bagSIPs.isChecked():
            bag_files = True
        scan_for_pii = False
        if self.bulkExt.isChecked():
            scan_for_pii = True

        # Create SIP for each source directory and write descriptive CSV.
        self.get_thread = SIPThread(
            dirs_to_process, sips, bag_files, scan_for_pii, destination
        )
        self.get_thread.increment_progress_bar["QString"].connect(
            self.increment_progress_bar
        )
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


if __name__ == "__main__":
    main()
