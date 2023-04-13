#!python

import sys
import pyxnat
from dax import XnatUtils

source_project = sys.argv[1]
dest_project = sys.argv[2]
subject = sys.argv[3]

with XnatUtils.InterfaceTemp() as xnat:

    # Subject variables
    source_subject = xnat.select(f'/projects/{source_project}/subjects/{subject}')
    dest_subject = xnat.select(f'/projects/{dest_project}/subjects/{subject}')

    dob = source_subject.attrs.get('xnat:demographicData/dob')
    gender = source_subject.attrs.get('xnat:demographicData/gender')
    handedness = source_subject.attrs.get('xnat:demographicData/handedness')
    race = source_subject.attrs.get('xnat:demographicData/race')
    #sid = source_subject.attrs.get("xnat:subjectData/fields/field[name='id']/field")
    sid = source_subject.xpath("/xnat:Subject/xnat:fields/xnat:field[@name='id']/text()[2]")[0]

    dest_subject.attrs.set('xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/dob', dob)
    dest_subject.attrs.set('xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/gender', gender)
    dest_subject.attrs.set('xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/handedness', handedness)
    dest_subject.attrs.set('xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/race', race)
    dest_subject.attrs.set("xnat:subjectData/fields/field[name='id']/field", sid)

    # Session variables
    source_session = xnat.select(f'/projects/{source_project}/subjects/{subject}/experiments/{subject}')
    dest_session = xnat.select(f'/projects/{dest_project}/subjects/{subject}/experiments/{subject}')

    sdate = source_session.attrs.get('xnat:mrSessionData/date')
    stime = source_session.attrs.get('xnat:mrSessionData/time')
    dest_session.attrs.set('xnat:mrSessionData/date',sdate)
    dest_session.attrs.set('xnat:mrSessionData/time',stime)

