#!python

import sys
import pyxnat
from dax import XnatUtils

source_project = sys.argv[1]
dest_project = sys.argv[2]
subject = sys.argv[3]

xnat = XnatUtils.InterfaceTemp()

# Subject variables
source_subject = xnat.select( 
    '/projects/{0}/subjects/{1}'.format(source_project,subject) )
dest_subject = xnat.select( 
    '/projects/{0}/subjects/{1}'.format(dest_project,subject) )

dob = source_subject.attrs.get('xnat:demographicData/dob')
gender = source_subject.attrs.get('xnat:demographicData/gender')
handedness = source_subject.attrs.get('xnat:demographicData/handedness')
race = source_subject.attrs.get('xnat:demographicData/race')
sid = source_subject.attrs.get("xnat:subjectData/fields/field[name='id']/field")

dest_subject.attrs.set('xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/dob', dob)
dest_subject.attrs.set('xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/gender', gender)
dest_subject.attrs.set('xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/handedness', handedness)
dest_subject.attrs.set('xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/race', race)
dest_subject.attrs.set("xnat:subjectData/fields/field[name='id']/field", sid)

# Session variables
source_session = xnat.select( 
    '/projects/{0}/subjects/{1}/experiments/{1}'.format(source_project,subject) )
dest_session = xnat.select( 
    '/projects/{0}/subjects/{1}/experiments/{1}'.format(dest_project,subject) )

sdate = source_session.attrs.get('xnat:mrSessionData/date')
stime = source_session.attrs.get('xnat:mrSessionData/time')
dest_session.attrs.set('xnat:mrSessionData/date',sdate)
dest_session.attrs.set('xnat:mrSessionData/time',stime)


# Clean up
xnat.disconnect()

