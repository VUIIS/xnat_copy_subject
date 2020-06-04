Copy scan data from one project to another on XNAT, for specified subjects and scan
types. Subject DOB, gender, handedness, race, and custom ID variable; session date 
and time; and scan DICOM resource are copied.

It is assumed that the session label is the same as the subject label - true for most
VUIIS studies, but not true in general.

DAX must be installed and its virtual environment activated. See
https://dax.readthedocs.io/en/latest/installing_dax_in_a_virtual_environment.html


Usage:

copy_subject.sh \
	--source_project <source_project> \
	--dest_project <destination_project> \
	--subjects 123456,234567,345678 \
	--scan_types "T1,DTI_HARDI" 
