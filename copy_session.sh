#!/bin/bash
#
# Copy certain DICOMs of a subject from one project to another on XNAT
#
# A DAX installation is required, and its python venv must be active.

# Parse options
while [[ $# -gt 0 ]]
do
	key="${1}"
	case "${key}" in
		--source_project)
			source_project="${2}"; shift; shift ;;
		--dest_project)
			dest_project="${2}"; shift; shift ;;
		--sessions)
			sessions="${2}"; shift; shift ;;
		--scan_types)
			scan_types="${2}"; shift; shift ;;
		--resources)
			resources="${2}"; shift; shift ;;
		*)
			echo Unknown input "${1}"; shift ;;
	esac
done

# Check for params
if [ -z "${source_project}" ] \
	|| [ -z "${dest_project}" ] \
    || [ -z "${sessions}" ] \
    || [ -z "${resources}" ] \
	|| [ -z "${scan_types}" ] ; then
	cat << HERE
Usage example:
    ${0} \\
      --source_project SOURCE_PROJ \\
      --dest_project DESTINATION_PROJ \\
      --sessions 123456,234567,345678 \\
      --resources NIFTI,JSON \\
      --scan_types T1,Rest
HERE
	exit 0
fi
	

# Where are our scripts? We need to find the python code
function realpath() {
    if ! pushd $1 &> /dev/null; then 
        pushd ${1##*/} &> /dev/null
        echo $( pwd -P )/${1%/*}
    else
        pwd -P
    fi
    popd > /dev/null
}
script_dir=$(realpath $(dirname "${0}"))


# Check for subjects already present in dest project
echo "Checking session list ${sessions}"
sesslist=$(echo ${sessions} | tr ',' ' ')
for sess in ${sesslist} ; do
	python "${script_dir}"/check_for_session.py "${dest_project}" "${sess}" \
	|| exit 1
done


# Make temporary directory
tmp_dir=$(mktemp -d copy_session.XXXXXX) || exit 1

# Download
Xnatdownload -p "${source_project}" -d "${tmp_dir}" \
    --sess "${sessions}" -s "${scan_types}" --rs "${resources}"

# Replace project name in download report CSV
cat "${tmp_dir}"/download_report.csv | \
	sed s/^scan,${source_project}/scan,${dest_project}/ > \
	"${tmp_dir}"/upload.csv

# Upload. Note, if target resource already exists, Xnatupload prints a warning and does
# not do the upload.
Xnatupload --csv "${tmp_dir}"/upload.csv

# Clean up
if [ -d "${tmp_dir}" -a -n "${tmp_dir}" ] ; then
	rm -fr "${tmp_dir}"
fi


# Set session dates
sesslist=$(echo ${sessions} | tr ',' ' ')
for sess in ${sesslist} ; do
	echo "Copying session dates for ${sess}"
		python "${script_dir}"/set_sess_vars.py "${source_project}" "${dest_project}" "${sess}"
done

