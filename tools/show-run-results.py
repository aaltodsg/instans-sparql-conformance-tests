#!/usr/bin/env python3

import os, sys
from csvtools import *

fields = ['base','type','suite','collection','name','queryfile','datafile','graphfiles','graphlabels','resultfile','resultgraphfiles','resultgraphlabels',
          'updateresult','queryserviceendpoint','queryservicedata','entailmentprofile','entailmentregime']

if len(sys.argv) != 5 and len(sys.argv) != 6:
    print('usage: {} <suite> <collection> <name> <field or extension>'.format(sys.argv[0]))
    print('fields: {}'.format(fields))
    print('extension: a relative path'.format(fields))
    sys.exit(1)

suite=sys.argv[1]
collection=sys.argv[2]
name=sys.argv[3]
tests=CSVfromFile('suites/tests-from-manifests.csv')
test=tests.select(lambda r: r['suite'] == suite and r['collection'] == collection and r['name'] == name)

if len(sys.argv) == 5:
    extension=''
    field=sys.argv[4]
else:
    extension=sys.argv[4]+'/'
    field=sys.argv[5]

if field in fields:
    fields=test.project(field)
    lines = [ 'suites/{}/{}/{}{}'.format(suite, collection, extension,r[field]) for r in fields.rows if r[field] != 'UNBOUND' ]
    for line in lines:
        print('{}'.format(line))
else:
    print('suites/{}/{}/{}{}'.format(suite,collection,extension,field))
                          


           
