#!python

import sys
import pyxnat
from dax import XnatUtils

dest_project = sys.argv[1]
subject = sys.argv[2]

with XnatUtils.InterfaceTemp() as xnat:
    dest_subject = xnat.select(f'/projects/{dest_project}/subjects/{subject}')
    if dest_subject.exists():
        raise Exception(f'Subject {subject} exists in project {dest_project}')
        sys.exit(1)
