import os

import bagit
import pytest

from main import SIPThread


def is_non_zero_file(filepath):
	return os.path.isfile(filepath) and os.path.getsize(filepath) > 0


def test_create_sip(tmp_path):
	OUTPUT_DIR = str(tmp_path / "output")
	DEST_DIR = str(tmp_path / "dest")

	for dir_ in (OUTPUT_DIR, DEST_DIR):
		os.makedirs(dir_)

	sip_thread = SIPThread(
		dirs_to_process=[os.path.abspath("./requirements")],
		destination=DEST_DIR,
		bag_files=False,
		scan_for_pii=False,
		output_dir=OUTPUT_DIR
	)
	sip_thread.run()

	assert is_non_zero_file(os.path.join(OUTPUT_DIR, "description.csv"))

	SIP_DIR = os.path.join(DEST_DIR, "requirements")
	OBJECTS_DIR = os.path.join(SIP_DIR, "objects")
	OBJECT_FILES_DIR = os.path.join(OBJECTS_DIR, "requirements")
	METADATA_DIR = os.path.join(SIP_DIR, "metadata")
	SUBDOC_DIR = os.path.join(METADATA_DIR, "submissionDocumentation")
	BRUNNHILDE_DIR = os.path.join(SUBDOC_DIR, "brunnhilde")

	assert is_non_zero_file(os.path.join(OBJECT_FILES_DIR, "base.txt"))
	assert is_non_zero_file(os.path.join(OBJECT_FILES_DIR, "test.txt"))

	assert os.path.isdir(BRUNNHILDE_DIR)
	assert is_non_zero_file(os.path.join(BRUNNHILDE_DIR, "report.html"))
	
	assert is_non_zero_file(os.path.join(SUBDOC_DIR, "dfxml.xml"))

	assert is_non_zero_file(os.path.join(METADATA_DIR, "checksum.md5"))


def test_create_sip_bagged(tmp_path):
	OUTPUT_DIR = str(tmp_path / "output")
	DEST_DIR = str(tmp_path / "dest")

	for dir_ in (OUTPUT_DIR, DEST_DIR):
		os.makedirs(dir_)

	sip_thread = SIPThread(
		dirs_to_process=[os.path.abspath("./requirements")],
		destination=DEST_DIR,
		bag_files=True,
		scan_for_pii=False,
		output_dir=OUTPUT_DIR
	)
	sip_thread.run()

	SIP_DIR = os.path.join(DEST_DIR, "requirements")
	OBJECTS_DIR = os.path.join(SIP_DIR, "data", "objects")
	OBJECT_FILES_DIR = os.path.join(OBJECTS_DIR, "requirements")
	METADATA_DIR = os.path.join(SIP_DIR, "data", "metadata")

	assert is_non_zero_file(os.path.join(OBJECT_FILES_DIR, "base.txt"))
	assert is_non_zero_file(os.path.join(OBJECT_FILES_DIR, "test.txt"))

	bag = bagit.Bag(SIP_DIR)
	assert bag.validate()

	assert not os.path.isfile(os.path.join(METADATA_DIR, "checksum.md5"))


def test_bulk_extractor(tmp_path):
	OUTPUT_DIR = str(tmp_path / "output")
	DEST_DIR = str(tmp_path / "dest")

	for dir_ in (OUTPUT_DIR, DEST_DIR):
		os.makedirs(dir_)

	sip_thread = SIPThread(
		dirs_to_process=[os.path.abspath("./requirements")],
		destination=DEST_DIR,
		bag_files=False,
		scan_for_pii=True,
		output_dir=OUTPUT_DIR
	)
	sip_thread.run()

	SIP_DIR = os.path.join(DEST_DIR, "requirements")
	OBJECTS_DIR = os.path.join(SIP_DIR, "objects")
	OBJECT_FILES_DIR = os.path.join(OBJECTS_DIR, "requirements")
	SUBDOC_DIR = os.path.join(SIP_DIR, "metadata", "submissionDocumentation")
	BRUNNHILDE_BE_DIR = os.path.join(SUBDOC_DIR, "brunnhilde", "bulk_extractor")

	assert is_non_zero_file(os.path.join(OBJECT_FILES_DIR, "base.txt"))
	assert is_non_zero_file(os.path.join(OBJECT_FILES_DIR, "test.txt"))

	assert is_non_zero_file(os.path.join(BRUNNHILDE_BE_DIR, "report.xml"))
