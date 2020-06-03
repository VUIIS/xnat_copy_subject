#!/bin/bash
#
# Copy certain DICOMs of a subject from one project to another on XNAT


# Parse options
while [[ $# -gt 0 ]]
do
	key="${1}"
	case "${key}" in
		--source_project)
			source_project="${2}"; shift; shift ;;
		--dest_project)
			dest_project="${2}"; shift; shift ;;
		--subjects)
			subjects="${2}"; shift; shift ;;
		--scan_types)
			scan_types="${2}"; shift; shift ;;
		*)
			echo Unknown input "${1}"; shift ;;
	esac
done

# Make temporary directory
tmp_dir=$(mktemp -d -t copy_subject) || exit 1

# Download
Xnatdownload -p "${source_project}" -d "${tmp_dir}" --subj "${subjects}" -s ${scan_types} --rs DICOM

# Replace project name in download report CSV
cat "${tmp_dir}"/download_report.csv | \
	sed s/^scan,${source_project}/scan,${dest_project}/ > \
	"${tmp_dir}"/upload.csv

# Upload
Xnatupload --csv "${tmp_dir}"/upload.csv

# Clean up
if [ -d "${tmp_dir}" ] ; then
	rm -fr "${tmp_dir}"
fi
