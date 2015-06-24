#!/usr/bin/env python3

import os, sys
from csvtools import *
from htmlgen import Division, Span

if len(sys.argv) != 4:
    print('usage: {} <suite> <collection> <name>'.format(sys.argv[0]))
    sys.exit(1)

suite=sys.argv[1]
collection=sys.argv[2]
name=sys.argv[3]

tests=CSVfromFile('suites/tests-from-manifests.csv')

#base,type,suite,collection,name,queryfile,datafile,graphfiles,graphlabels,resultfile,resultgraphfiles,resultgraphlabels,updateresult,queryserviceendpoint,queryservicedata,entailmentprofile,entailmentregime

test=tests.select(lambda r: r['suite'] == suite and r['collection'] == collection and r['name'] == name).rows[0].items
page = markup.page( )
id='{}/{}/{}'.format(suite,collection,name)
page.init( title=id )
#page.h1('{}'.format(id))
print(page)



           
