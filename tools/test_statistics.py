#!/usr/bin/env python3 
import os, sys
from csvtools import *

# Input tables
input_file = sys.argv[1]

# Output tables go to the same directory where input came from

output_dir = os.path.dirname(input_file)

suite_file = os.path.join(output_dir, "suite.csv")
suite_collection_file = os.path.join(output_dir, "suite-collection.csv")
type_file = os.path.join(output_dir, "type.csv")
suite_collection_double_type_file = os.path.join(output_dir, "suite-collection-double-type.csv")
not_implemented_file = os.path.join(output_dir, "not-implemented.csv")
implemented_undefined_file  = os.path.join(output_dir, "implemented_undefined.csv")
negative_syntax_parsed_file = os.path.join(output_dir, "negative-syntax-parsed.csv")
negative_syntax_parsed_undefined_file = os.path.join(output_dir, "negative-syntax-parsed-undefined.csv")
positive_syntax_not_parsed_file = os.path.join(output_dir, "positive-syntax-not-parsed.csv")
positive_syntax_parsed_undefined_file = os.path.join(output_dir, "positive-syntax-parsed-undefined.csv")
positive_syntax_parsed_not_translated_file = os.path.join(output_dir, "positive-syntax-parsed-not-translated.csv")
positive_syntax_parsed_translated_undefined_file = os.path.join(output_dir, "positive-syntax-parsed-translated-undefined.csv")
positive_syntax_parsed_translated_not_initialized_file = os.path.join(output_dir, "positive-syntax-parsed-translated-not-initialized.csv")
positive_syntax_parsed_translated_initialized_undefined_file = os.path.join(output_dir, "positive-syntax-parsed-translated-initialized-undefined.csv")
query_not_runnable_file = os.path.join(output_dir, "query-not-runnable.csv")
query_runnable_undefined_file = os.path.join(output_dir, "query-runnable-undefined.csv")
query_runnable_not_implemented_file = os.path.join(output_dir, "query-runnable-not-implemented.csv")
query_runnable_implemented_undefined_file = os.path.join(output_dir, "query-runnable-implemented-undefined.csv")
query_runnable_implemented_not_ran_file = os.path.join(output_dir, "query-runnable-implemented-not-ran.csv")
query_runnable_implemented_ran_undefined_file = os.path.join(output_dir, "query-runnable-implemented-ran-undefined.csv")
query_runnable_implemented_ran_not_compared_file = os.path.join(output_dir, "query-runnable-implemented-ran-not-compared.csv")
query_runnable_implemented_ran_compared_undefined_file = os.path.join(output_dir, "query-runnable-implemented-ran-compared-undefined.csv")
failed_file = os.path.join(output_dir, "failed.csv")
failed_undefined_file  = os.path.join(output_dir, "failed_undefined.csv")

# Read inputs

all = CSVfromFile(input_file, message='Input {}')
print('\nTest suite, collection, and type statistics:')
print('* {} tests. See {}'.format(len(all), input_file))
suite = all.project('suite').dropDuplicates()
print('* {} test suites. See {}'.format(len(suite), suite_file))
suite.write(suite_file)
suite_collection = all.project('suite','collection').dropDuplicates()
print('* {} test collections. See {}'.format(len(suite_collection), suite_collection_file))
suite_collection.write(suite_collection_file)
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
print('* {} types. See {}'.format(len(types), type_file))

suite_collection_type = all.project('type','suite','collection').dropDuplicates()
def csrows(g,rows):
    headers = ['suite','collection','type1','type2']
#     if len(rows) == 1:
#         return CSV(headers,[[g[0],g[1],rows[0]['type'],'']])
    if len(rows) == 2:
        return CSV(headers,[[g[0],g[1],rows[0]['type'],rows[1]['type']]])
#    raise Exception("More than 2 types for {}".format(g))
    return CSV(headers, [])
suite_collection_double_type=suite_collection_type.aggregate(suite_collection_type.fieldsPartitioner(['suite','collection']),csrows).sort('suite')
print('* {} collections with two types. See {}'.format(len(suite_collection_double_type), suite_collection_double_type_file))
suite_collection_double_type.write(suite_collection_double_type_file)

def check_counts(part1, part2, total, indent, dp1, dp2, dtot, difference_file=None):
    diff1=total.minus(part1.union(part2))
    if len(diff1) > 0:
        print(format('='+'='*indent+'> len({}):{} > {} = len({}):{} + len({}):{}!'.format(dtot, len(total), len(part1) + len(part2), dp1, len(part1), dp2, len(part2))+(' See '+difference_file if difference_file else '')))
        if difference_file: diff1.write(difference_file)
        return False
    diff2=part1.union(part2).minus(total)
    if len(diff2) > 0:
        print(format('='+'='*indent+'> len({}):{} < {} = len({}):{} + len({}):{}!'.format(dtot, len(total), len(part1) + len(part2), dp1, len(part1), dp2, len(part2))+(' See '+difference_file if difference_file else '')))
        if difference_file: diff2.write(difference_file)
        return False

print('\nTest execution statistics:')
print('\n* {:>4} tests in total'.format(len(all)))
not_implemented = all.select(lambda r:r['implementedp'] == 'False')
if len(not_implemented) > 0:
    print('--> {} test not executed, because features not implemented in INSTANS. See {}'.format(len(not_implemented), not_implemented_file))
    not_implemented.write(not_implemented_file)
implemented = all.select(lambda r:r['implementedp'] == 'True')
check_counts(implemented, not_implemented, all, 6, 'tests implemented', 'tests not implemented', 'all tests', implemented_undefined_file)

print('\nSyntax test execution statistics:')
syntax = all.select(lambda r:r['syntax-test-p'] == 'True')
print('\n*{:>4} syntax tests.'.format(len(syntax)))
negative_syntax = syntax.select(lambda r: r['negative-syntax-test-p'] == 'True')
print('      * {} negative syntax tests.'.format(len(negative_syntax)))
negative_syntax_parsed = negative_syntax.select(lambda r: r['parsing-succeeded-p'] == 'True')
if len(negative_syntax_parsed) > 0:
    print('------------> {:>3} negative syntax tests unexpectedly parsed! See {}'.format(len(negative_syntax_parsed), negative_syntax_parsed_file))
    negative_syntax_parsed.write(negative_syntax_parsed_file)
negative_syntax_not_parsed = negative_syntax.select(lambda r: r['parsing-succeeded-p'] == 'False')
print('            * {:>3} negative syntax tests did not parse.'.format(len(negative_syntax_not_parsed)))
check_counts(negative_syntax_parsed, negative_syntax_not_parsed, negative_syntax, 12, 'negative syntax parsed ', 'negative syntax not parsed ', 'negative syntax', negative_syntax_parsed_undefined_file)


positive_syntax = syntax.select(lambda r: r['negative-syntax-test-p'] == 'False')
print('      * {} positive syntax tests.'.format(len(positive_syntax)))
positive_syntax_not_parsed = positive_syntax.select(lambda r: r['parsing-succeeded-p'] == 'False')
if len(positive_syntax_not_parsed) > 0:
    print('-------------> {} positive syntax tests did not parse! See {}'.format(len(positive_syntax_not_parsed), positive_syntax_not_parsed_file))
    positive_syntax_not_parsed.write(positive_syntax_not_parsed_file)

positive_syntax_parsed = positive_syntax.select(lambda r: r['parsing-succeeded-p'] == 'True')
print('            * {} positive syntax tests parsed.'.format(len(positive_syntax_parsed)))
check_counts(positive_syntax_not_parsed, positive_syntax_parsed, positive_syntax, 12, 'positive syntax not parsed', 'positive syntax parsed', 'positive syntax', positive_syntax_parsed_undefined_file)

positive_syntax_parsed_not_translated = positive_syntax_parsed.select(lambda r: r['translation-succeeded-p'] == 'False')
if len(positive_syntax_parsed_not_translated) > 0:
    print('------------------> {:>3} positive syntax tests parsed, but did not translate! See {}'.format(len(positive_syntax_parsed_not_translated), positive_syntax_parsed_not_translated_file))
    positive_syntax_parsed_not_translated.write(positive_syntax_parsed_not_translated_file)
positive_syntax_parsed_translated = positive_syntax_parsed.select(lambda r: r['translation-succeeded-p'] == 'True')
print('                  * {:>3} positive syntax tests parsed and translated.'.format(len(positive_syntax_parsed_translated)))
check_counts(positive_syntax_parsed_translated, positive_syntax_parsed_not_translated, positive_syntax_parsed, 18, 'positive syntax parsed translated', 'positive syntax parsed not translated', 'positive syntax parsed', positive_syntax_parsed_translated_undefined_file)

positive_syntax_parsed_translated_not_initialized = positive_syntax_parsed_translated.select(lambda r: r['initialization-succeeded-p'] == 'False')
if len(positive_syntax_parsed_translated_not_initialized) > 0:
    print('------------------------> {:>3} positive syntax tests parsed and translated, but did not initialize! See {}'.format(len(positive_syntax_parsed_translated_not_initialized), positive_syntax_parsed_translated_not_initialized_file))
    positive_syntax_parsed_translated_not_initialized.write(positive_syntax_parsed_translated_not_initialized_file)
positive_syntax_parsed_translated_initialized = positive_syntax_parsed_translated.select(lambda r: r['initialization-succeeded-p'] == 'True')
print('                        * {:>3} positive syntax tests parsed, translated and initialized.'.format(len(positive_syntax_parsed_translated_initialized)))
check_counts(positive_syntax_parsed_translated_initialized, positive_syntax_parsed_translated_not_initialized, positive_syntax_parsed_translated, 24, 'positive syntax parsed translated initialized', 'positive syntax parsed translated not initialized', 'positive syntax parsed translated', positive_syntax_parsed_translated_initialized_undefined_file)

print('\nQuery evalution test execution statistics:')
query = syntax.select(lambda r: r['query-evaluation-test-p'] == 'True')
print('\n*{:>4} query evaluation tests.'.format(len(query)))
query_not_runnable = query.minus(positive_syntax_parsed_translated_initialized)
print('------> {:>3} query evaluation tests not runnable (not parsed, translated, or initialized).'.format(len(query_not_runnable)))
query_runnable = query.intersection(positive_syntax_parsed_translated_initialized)
print('      * {:>3} query evaluation tests runnable (parsed, translated, initialized).'.format(len(query_runnable)))
check_counts(query_runnable, query_not_runnable, query, 6, 'query runnable', 'query not runnable', 'query', query_runnable_undefined_file)

query_runnable_not_implemented = query_runnable.select(lambda r: r['implementedp'] != 'True')
if len(query_runnable_not_implemented) > 0:
    print('------------> {:>3} runnable query evaluation tests with non-implemented operations in INSTANS! See {}'.format(len(query_runnable_not_implemented), query_runnable_not_implemented_file))
    query_runnable_not_implemented.write(query_runnable_not_implemented_file)
query_runnable_implemented = query_runnable.select(lambda r: r['implementedp'] == 'True')
print('            * {:>3} query_runnable evaluation tests fully implemented in INSTANS.'.format(len(query_runnable_implemented)))
check_counts(query_runnable_implemented, query_runnable_not_implemented, query_runnable, 6, 'query runnable implemented', 'query runnable not implemented', 'query runnable', query_runnable_implemented_undefined_file)

query_runnable_implemented_not_ran = query_runnable_implemented.select(lambda r: r['running-succeeded-p'] == 'False')
if len(query_runnable_implemented_not_ran) > 0:
    print('------------------> {:>3} query runnable evaluation tests fully implemented in INSTANS, but dit not run!'.format(len(query_runnable_implemented_not_ran), query_runnable_implemented_not_ran_file))
    query_runnable_implemented_not_ran.write(query_runnable_implemented_not_ran_file)
query_runnable_implemented_ran = query_runnable_implemented.select(lambda r: r['running-succeeded-p'] == 'True')
print('                  * {:>3} query runnable evaluation tests implemented and ran.'.format(len(query_runnable_implemented_ran)))
check_counts(query_runnable_implemented_ran, query_runnable_implemented_not_ran, query_runnable_implemented, 18, 'query runnable implemented ran', 'query runnable implemented not ran', 'query runnable implemented', query_runnable_implemented_ran_undefined_file)

query_runnable_implemented_ran_not_compared = query_runnable_implemented.select(lambda r: r['comparing-succeeded-p'] == 'False')
if len(query_runnable_implemented_ran_not_compared) > 0:
    print('------------------------> {:>3} query runnable evaluation tests fully implemented in INSTANS, ran, but dit not compare!'.format(len(query_runnable_implemented_ran_not_compared), query_runnable_implemented_ran_not_compared_file))
    query_runnable_implemented_ran_not_compared.write(query_runnable_implemented_ran_not_compared_file)
query_runnable_implemented_ran_compared = query_runnable_implemented.select(lambda r: r['comparing-succeeded-p'] == 'True')
print('                        * {:>3} query runnable evaluation tests implemented ran and compared.'.format(len(query_runnable_implemented_ran_compared)))
check_counts(query_runnable_implemented_ran_compared, query_runnable_implemented_ran_not_compared, query_runnable_implemented_ran, 24, 'query runnable implemented ran compared', 'query runnable implemented ran not compared', 'query runnable implemented ran', query_runnable_implemented_ran_compared_undefined_file)

print('\nSummary')
print('\n* {:>4} tests in total'.format(len(all)))
failed = all.select(lambda r:r['failedp'] == 'True')
if len(failed) > 0:
    print('-------> {} tests failed. See {}'.format(len(failed), failed_file))
    failed.write(failed_file)
not_failed = all.select(lambda r:r['failedp'] == 'False')
print('       * {:>3} tests succeeded.'.format(len(not_failed)))
check_counts(failed, not_failed, all, 6, 'tests failed', 'tests not failed', 'all tests', failed_undefined_file)
sys.exit(0)
