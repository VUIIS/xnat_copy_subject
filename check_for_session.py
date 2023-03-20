#!python

import sys
import pyxnat
from dax import XnatUtils

dest_project = sys.argv[1]
session = sys.argv[2]

with XnatUtils.InterfaceTemp() as xnat:

    dest_session = xnat.select(f'/projects/{dest_project}/subjects/{session}')

    if dest_session.exists():
        raise Exception(f'Session {session} exists in project {dest_project}')
        sys.exit(1)
