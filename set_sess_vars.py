#!python

import sys
import pyxnat
from dax import XnatUtils

source_project = sys.argv[1]
dest_project = sys.argv[2]
session = sys.argv[3]

with XnatUtils.InterfaceTemp() as xnat:

    # Session variables
    source_session = xnat.select(f'/projects/{source_project}/experiments/{session}' )
    dest_session = xnat.select(f'/projects/{dest_project}/experiments/{session}' )

    sdate = source_session.attrs.get('xnat:mrSessionData/date')
    stime = source_session.attrs.get('xnat:mrSessionData/time')
    dest_session.attrs.set('xnat:mrSessionData/date',sdate)
    dest_session.attrs.set('xnat:mrSessionData/time',stime)

