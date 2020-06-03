#!/bin/bash
#
# Copy certain DICOMs of a subject from MORGAN project to MORGAN_DWI project on XNAT
#
# Usage:
#    copy_subject.sh <subject_id>
#
# Example:
#    copy_subject.sh 

subject=${1}

# Source project
source_proj=

# Destination project
dest_proj=

# Labels of scans to copy - comma-separated list
scan_types="AnatBrain_T1W3D,DTI_HARD_2.5_iso,HARDI_2.5_iso,rDTI_APA_2.5iso"

# Make temporary directory
tmp_dir=$(mktemp -d -t copy_subject) || exit 1

# Download
Xnatdownload -p "${source_proj}" -d "${tmp_dir}" --subj "${subject}" -s ${scan_types} --rs DICOM

# Replace project name in download report CSV
cat "${tmp_dir}"/download_report.csv | sed s/^scan,${source_proj}/scan,${dest_proj}/ > "${tmp_dir}"/upload.csv

# Upload
Xnatupload --csv "${tmp_dir}"/upload.csv

# Clean up
if [ -d "${tmp_)dir}" ] ; then
	rm -fr "${tmp_dir}"
fi
