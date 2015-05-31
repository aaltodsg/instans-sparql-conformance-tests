# Author: Esko Nuutila (esko.nuutila@iki.fi), 2014-2015.

import sys
import csv
import operator

class CSVException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Row():
    def __init__(self, csv, items=[]):
        self.csv = csv
        self.items = list(items)

    def fieldIndex(self, field):
#        print('fieldIndex(field=', field, ')')
        res = field if isinstance(field, int) else self.csv.headers.items.index(field)
#        print(' -> ', res)
        return res

    # Delegate all behavior to the list 'items'
    def __len__(self)                 : return len(self.items)
    def __iter__(self)                : return iter(self.items)
    def __contains__(self, item)      : return item in self.items
    def __str__(self)                 : return "Row([" + ",".join(["'"+str(i)+"'" for i in self.items]) + "])"
    def __eq__(self, other)           : return self.items == other.items
    def index(self, value)            : return self.items.index(value)
    def __add__(self, other)          : return self.items + (other.items if isinstance(other,Row) else other) # Slight misuse.
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.items.__getitem__(key)
        else:
            return self.items[self.fieldIndex(key)]
    def __setitem__(self, key, value):
        if isinstance(key, slice):
            return self.items.__setitem__(key, value)
        else:
            self.items[self.fieldIndex(key)] = value

class CSV():
    def __init__(self, headers, rows):
        '''headers can be either a Row or a sequence and rows can be a sequence of Rows or sequences'''
#        print(headers)
        self.headers = Row(self, headers.items if isinstance(headers, Row) else headers)
#        print(self.headers)
        self.rows = [ Row(self, row.items if isinstance(row, Row) else row) for row in rows ]
        self.check()

    # def strip(self, chars=' \t'):
    #     return self.map([ lambda x: x.strip(chars) for i in range(len(self.headers)) ])

    def __len__(self)                 : return len(self.rows)

    def row(self, key):
        result = self.select(lambda r: r[0] == key)
        if len(result.rows) == 0:
            raise CSVException('No results with key {}'.format(key))
        elif len(result.rows) > 1:
            raise CSVException('More than one results with key {}'.format(key))
        else:
            return result.rows[0]

    def column(self, key):
        return [ row[key] for row in self.rows]

    def replaceHeaders(self, newheaders):
        if isinstance(newheaders, dict):
            for (old, new) in newheaders.items():
                self.headers[old]=new
        else:
            if len(newheaders) != len(self.headers):
                raise CSVException('Length of new headers {} not equal to the length of old headers {}'.format(newheaders, self.headers.items))
            self.headers = Row(self, newheaders)

    def check(self):
        if any(row for row in self.rows if len(row) != len(self.headers)):
            print("Error:")
            print(self.headers, "length = ", len(self.headers))
            for row in self.rows: print(row, "length = ", len(row))
            raise ValueError("Mismatching row lengths")

    def select(self, test=lambda x: True):
        return CSV(self.headers, [ row for row in self.rows if test(row) ])

    def project(self, *fields):
        """takes either a list of field names/indices or field names/indices as positional parameters"""
        if len(fields) == 1 and isinstance(fields[0], list):
            fields = fields[0]
        return CSV([ self.headers[field] for field in fields ],
                   [ [ row[field] for field in fields ] for row in self.rows ])

    def projectNot(self, *drop):
        """takes either a list of field names/indices or field names/indices as positional parameters"""
        if len(drop) == 1 and isinstance(drop[0], list):
            drop = drop[0]
        fields = [ f for f in self.headers if f not in drop ]
        return CSV([ self.headers[field] for field in fields ],
                   [ [ row[field] for field in fields ] for row in self.rows ])

    def join(self, other, test=None, field=None, fields=None):
        headers = self.headers + [ h for h in other.headers if h not in self.headers ]
        if test == None:
            test = lambda r1, r2: all(( r1[field] == r2[field] for f in ( ( field, ) if field else (fields or ( h for h in self.headers if h in other.headers )))))
        return CSV(self.headers + other.headers, [ r1 + r2 for r1 in self.rows for r2 in other.rows if test(r1, r2) ]).project(headers)

    def leftJoin(self, other, test=None, field=None, fields=None):
        headers = self.headers + [ h for h in other.headers if h not in self.headers ]
        if test == None:
            test = lambda r1, r2: all(( r1[field] == r2[field] for f in ( ( field, ) if field else (fields or ( h for h in self.headers if h in other.headers )))))
        return CSV(self.headers + other.headers,
                   [ r1 + r2 for r1 in self.rows for r2 in ( [ r for r in other.rows if test(r1, r) ]
                                                             or [ ['']*len(other.headers) ] ) ] ).project(headers)

    def union(self, other):
        if self.headers != other.headers:
            raise ValueError("Incompatible tables")
        rows = [row for row in self.rows]
        for row in other.rows:
            if row not in rows:
                rows.append(row)
        return CSV(self.headers, rows)

    def minus(self, other):
        if self.headers != other.headers:
            raise ValueError("Incompatible tables")
        rows = [row for row in self.rows]
        for row in other.rows:
            if row in rows:
                rows.remove(row)
        return CSV(self.headers, rows)

    def dropDuplicates(self):
        return CSV(self.headers, []).union(self)

    def hasDuplicates(self):
        return len(self.minus(self.dropDuplicates())) > 0

    def sort(self, field, reverseOrder=False, unique=False):
        sortedRows = sorted(self.rows, key=lambda row: row[field], reverse = reverseOrder)
        if unique and sortedRows:
            prev = sortedRows.pop()
            uniqueRows = [ prev ]
            for row in sortedRows:
                if row != prev:
                    uniqueRows.append(row)
                    prev = row
            sortedRows = uniqueRows
        return CSV(self.headers, sortedRows)

    #def write(self, file, quoting=csv.QUOTE_ALL):
    def write(self, fname, quoting=csv.QUOTE_MINIMAL, delimiter=',', message=None):
        if message:
            print(message.format(fname))
        with open(fname, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=quoting,lineterminator='\n', delimiter=delimiter)
            writer.writerow(self.headers)
            for row in self.rows:
                writer.writerow(row)

    def show(self, quoting=csv.QUOTE_MINIMAL, delimiter=',', message=None):
        if message:
            print(message)
        writer = csv.writer(sys.stdout, quoting=quoting,lineterminator='\n', delimiter=delimiter)
        writer.writerow(self.headers)
        for row in self.rows:
            writer.writerow(row)

    def findRow(self, field, value):
        return next((row for row in self.rows if row[field] == value), None)

    def fieldFunc(self, field, func):
        return [ func if i == self.headers.fieldIndex(field) else lambda x: x for i in range(len(self.headers.items))]

    def map(self, func):
        if callable(func):
            return CSV(self.headers, [ func(row) for row in self.rows ])
        else:
            return CSV(self.headers, [ [ fieldfunc(field) for fieldfunc,field in zip(func,row.items)] for row in self.rows ])

    def mapField(self, field, func):
        return self.map(self.fieldFunc(field, func))

    def transform(self, newHeaders, func):
        return CSV(newHeaders, [ func(row) for row in self.rows ])

    def transpose(self, h0):
        tHeaders = [ h0 ] + [ row[0] for row in self.rows ]
        tRows = [ [ name ] + [ row[name] for row in self.rows] for name in self.headers[1:]]
        return CSV(tHeaders, tRows)

    # Partitioner can return any kind of items that aggregator can take as its first parameter
    # Aggregator MUST return CSVs with same headers
    def aggregate(self, partitioner, aggregator):
        groups = {}
        for row in self.rows:
            group = partitioner(row)
#            print('Group: {}'.format(group))
            if group in groups:
                groups[group].append(row)
            else:
                groups[group] = [row]
        arows = []
#        for g,r in groups: print('{}: {}'.format(g, r))
        result = None
        for group,rows in groups.items():
#            print('group = {}, rows = {}'.format(group, rows))
            if result:
                result = result.union(aggregator(group, rows))
            else:
                result = aggregator(group, rows)
        return result

    def maximize(self, dataField, *idFields):
        def groupMaxRow(group, rows):
            sorted = CSV(self.headers, rows).sort(dataField, reverseOrder=True)
            return CSV(self.headers, [ sorted.rows[0]])
        return self.aggregate(self.fieldsPartitioner(idFields), groupMaxRow)

    def fieldsPartitioner(self, fields):
        return lambda row: tuple(( row[field] for field in fields ))

    def fieldPartitioner(self, field):
        return lambda row: row[field]

    def computeField(self, resultField, func):
        nh = self.headers.items+[resultField]
        nr = [ row + [func(row)] for row in self.rows]
        return CSV(nh, nr)

    def computeFields(self, resultFields, func):
        nh = self.headers.items+resultFields
        nr = [ row + func(row) for row in self.rows]
        return CSV(nh, nr)

    def aggregateFields(self, resultField, fieldConvert, aggrFunc, fields):
        return self.computeField(resultField, lambda row: aggrFunc([fieldConvert(row[f]) for f in self.headers if f in fields]))

    def sumFields(self, resultField, fieldConvert, fields):
        return self.aggregateFields(resultField, fieldConvert, sum, fields)

class CSVfromFile(CSV):
    def __init__(self, fname, skipLines=0, message=None, strip=True, sniffDialect=True, **dialectArgs):
        self.filename = fname
        if message:
            print(message.format(fname))
        with open(fname, 'r', encoding='utf-8') as csvfile:
            for i in range(skipLines): repr(csvfile.readline())
            if sniffDialect:
                try:
                    dialect = csv.Sniffer().sniff(csvfile.read(2048))
                except csv.Error:
                    dialect = 'unix'
            else:
                dialect = csv.Dialect('unix', **dialectArgs)
            csvfile.seek(0)
            lines = list(iter(csv.reader(csvfile, dialect)))
            if strip:
                lines = [ [ value.strip() for value in line] for line in lines ]
            CSV.__init__(self, lines[0], lines[1:])
