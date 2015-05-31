#!/usr/bin/env python3 
import os, sys
from csvtools import *

all = CSVfromFile(sys.argv[1], message='Input {}')
print('\nTest suite, collection, and type statistics:')
print('\nTotal {} tests'.format(len(all)))
suite = all.project('suite').dropDuplicates()
print('\n{} test suites:'.format(len(suite)))
suite.show()
suite_collection = all.project('suite','collection').dropDuplicates()
print('\n{} test collections:'.format(len(suite_collection)))
suite_collection.show()
# QueryEvaluationTest
# PositiveSyntaxTest
# NegativeSyntaxTest
# UpdateEvaluationTest
# NegativeSyntaxTest11
# CSVResultFormatTest
# ProtocolTest
# ServiceDescriptionTest
# PositiveSyntaxTest11
# PositiveUpdateSyntaxTest11
# NegativeUpdateSyntaxTest11
types=all.project('type').sort('type',unique=True)
print('\n{} types:'.format(len(types)))
types.show()

suite_collection_type = all.project('type','suite','collection').dropDuplicates()
def csrows(g,rows):
    headers = ['suite','collection','type1','type2']
#     if len(rows) == 1:
#         return CSV(headers,[[g[0],g[1],rows[0]['type'],'']])
    if len(rows) == 2:
        return CSV(headers,[[g[0],g[1],rows[0]['type'],rows[1]['type']]])
#    raise Exception("More than 2 types for {}".format(g))
    return CSV(headers, [])
sct=suite_collection_type.aggregate(suite_collection_type.fieldsPartitioner(['suite','collection']),csrows).sort('suite')
print('\n{} collections with two types:'.format(len(sct)))
sct.show()

print('\nTest execution statistics:')
not_implemented = all.select(lambda r:r['implementedp'] == 'False')
print('\n{} test not executed, because features not implemented in INSTANS:'.format(len(not_implemented)))
not_implemented.project('suite','collection','name','type').show()

print('\nSyntax test execution statistics:')
syntax = all.select(lambda r:r['syntax-test-p'] == 'True')
print('\n*{:>4} syntax tests.'.format(len(syntax)))
negative_syntax = syntax.select(lambda r: r['negative-syntax-test-p'] == 'True')
print('      * {} negative syntax tests.'.format(len(negative_syntax)))
negative_syntax_parsed = negative_syntax.select(lambda r: r['parsing-succeeded-p'] == 'True')
print('------> {:>3} negative syntax tests parsed!'.format(len(negative_syntax_parsed)))
positive_syntax = syntax.select(lambda r: r['negative-syntax-test-p'] == 'False')
print('      * {} positive syntax tests.'.format(len(positive_syntax)))
positive_syntax_not_parsed = positive_syntax.select(lambda r: r['parsing-succeeded-p'] == 'False')
print('------------> {:>3} positive syntax tests not parsed!'.format(len(positive_syntax_not_parsed)))
positive_syntax_parsed = positive_syntax.select(lambda r: r['parsing-succeeded-p'] == 'True')
print('            * {} positive syntax tests parsed.'.format(len(positive_syntax_parsed)))
positive_syntax_parsed_not_translated = positive_syntax_parsed.select(lambda r: r['translation-succeeded-p'] == 'False')
print('------------------> {:>3} positive syntax tests parsed, but not translated!'.format(len(positive_syntax_parsed_not_translated)))
positive_syntax_parsed_translated = positive_syntax_parsed.select(lambda r: r['translation-succeeded-p'] == 'True')
print('                  * {:>3} positive syntax tests parsed and translated.'.format(len(positive_syntax_parsed_translated)))
positive_syntax_parsed_translated_not_initialized = positive_syntax_parsed_translated.select(lambda r: r['initialization-succeeded-p'] == 'False')
print('------------------------> {:>3} positive syntax tests not initialized!'.format(len(positive_syntax_parsed_translated_not_initialized)))
positive_syntax_parsed_translated_initialized = positive_syntax_parsed_translated.select(lambda r: r['initialization-succeeded-p'] == 'True')
print('                        * {:>3} positive syntax tests initialized.'.format(len(positive_syntax_parsed_translated_initialized)))
print('\nQuery evalution test execution statistics:')
# query = all.select(lambda r: r['query-evaluation-test-p'] == 'True')
# print('\n*{:>4} query evaluation tests.'.format(len(query)))
query = syntax.select(lambda r: r['query-evaluation-test-p'] == 'True')
print('\n*{:>4} query evaluation tests.'.format(len(query)))
query_not_ran = query.select(lambda r: r['running-succeeded-p'] == 'False')
print('------------> {:>3} query evaluation tests not ran!'.format(len(query_not_ran)))
query_ran = query.select(lambda r: r['running-succeeded-p'] == 'True')
print('            * {:>3} query evaluation tests ran.'.format(len(query_ran)))
query.select(lambda r: r['running-succeeded-p'] not in {'True','False'}).project('type','suite','collection','name','running-succeeded-p').show()



sys.exit(0)




