#!/usr/bin/env python3 
import os, sys
from csvtools import *

mem=CSVfromFile('mem.csv')
biggest=CSV(['mem','size'],[ [ name, int(size) ] for (name, size) in zip(mem.headers.items,mem.rows[-1].items) ]).sort('size',reverseOrder=True).show()
