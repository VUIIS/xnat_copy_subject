#!/usr/bin/env python

import sys
import pyxnat
from dax import XnatUtils

dest_project = sys.argv[1]
subject = sys.argv[2]

xnat = XnatUtils.InterfaceTemp()

# Subject variables
dest_subject = xnat.select( 
    '/projects/{0}/subjects/{1}'.format(dest_project,subject) )

if dest_subject.exists():
    xnat.disconnect()
    raise Exception('Subject {0} exists in project {1}'.format(subject,dest_project))
    sys.exit(1)

xnat.disconnect()
