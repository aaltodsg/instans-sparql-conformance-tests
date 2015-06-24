#!/usr/bin/env python3 
import os, sys
from csvtools import *

if len(sys.argv) != 3:
    print('usage: {} <test-result-csv> <statistics output dir>'.format(sys.argv[0]))
    sys.exit(1)

# script inputs
input_file = sys.argv[1]
output_dir = sys.argv[2]

# Output tables go to the same directory where input came from

(root, ext) = os.path.splitext(input_file)
allsanstimesfile = root+'-sans-times'+ext
output_msgs = os.path.join(output_dir, "results.txt")
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
query_runnable_implemented_ran_different_semantics_file = os.path.join(output_dir, "query-runnable-implemented-ran-different-semantics.csv")
query_runnable_implemented_ran_not_compared_file = os.path.join(output_dir, "query-runnable-implemented-ran-not-compared.csv")
query_runnable_implemented_ran_compared_undefined_file = os.path.join(output_dir, "query-runnable-implemented-ran-compared-undefined.csv")
failed_file = os.path.join(output_dir, "failed.csv")
failed_undefined_file  = os.path.join(output_dir, "failed_undefined.csv")
failed_implemented_file = os.path.join(output_dir, "failed-implemented.csv")
failed_not_implemented_file = os.path.join(output_dir, "failed-not-implemented.csv")

if os.path.exists(output_msgs):
    os.remove(output_msgs)

def write_non_empty(cvs, file):
    if len(cvs) > 0:
        cvs.write(file)

def msg(txt):
    with open(output_msgs, 'a') as o:
        o.write(txt+'\n')
        print(txt)

refs=[]

def see(file, prefix=' See '):
    global refs
    refs.append(file)
    return '{}[{}]'.format(prefix, len(refs))

def check_counts(part1, part2, total, indent, dp1, dp2, dtot, difference_file=None):
    diff1=total.minus(part1.union(part2))
    if len(diff1) > 0:
        msg(format('='+'='*indent+'> len({}):{} > {} = len({}):{} + len({}):{}!'.format(dtot, len(total), len(part1) + len(part2), dp1, len(part1), dp2, len(part2))+see(difference_file if difference_file else '')))
        if difference_file: diff1.write(difference_file)
        return False
    diff2=part1.union(part2).minus(total)
    if len(diff2) > 0:
        msg(format('='+'='*indent+'> len({}):{} < {} = len({}):{} + len({}):{}!'.format(dtot, len(total), len(part1) + len(part2), dp1, len(part1), dp2, len(part2))+see(difference_file if difference_file else '')))
        if difference_file: diff2.write(difference_file)
        return False

# Read inputs

all = CSVfromFile(input_file, message='Input {}')
allsanstimes=all.projectNot('time')
allsanstimes.write(allsanstimesfile, message='Write {}')
suite = allsanstimesproject('suite').dropDuplicates()
suite_collection = allsanstimesproject('suite','collection').dropDuplicates()
types=allsanstimesproject('type').sort('type',unique=True)
suite_collection_type = allsanstimesproject('type','suite','collection').dropDuplicates()
def csrows(g,rows):
    headers = ['suite','collection','type1','type2']
#     if len(rows) == 1:
#         return CSV(headers,[[g[0],g[1],rows[0]['type'],'']])
    if len(rows) == 2:
        return CSV(headers,[[g[0],g[1],rows[0]['type'],rows[1]['type']]])
#    raise Exception("More than 2 types for {}".format(g))
    return CSV(headers, [])
suite_collection_double_type=suite_collection_type.aggregate(suite_collection_type.fieldsPartitioner(['suite','collection']),csrows).sort('suite')
not_implemented = allsanstimesselect(lambda r:r['implementedp'] == 'False')
implemented = allsanstimesselect(lambda r:r['implementedp'] == 'True')
syntax = allsanstimesselect(lambda r:r['syntax-test-p'] == 'True')
negative_syntax = syntax.select(lambda r: r['negative-syntax-test-p'] == 'True')
negative_syntax_parsed = negative_syntax.select(lambda r: r['parsing-succeeded-p'] == 'True')
negative_syntax_not_parsed = negative_syntax.select(lambda r: r['parsing-succeeded-p'] == 'False')
positive_syntax = syntax.select(lambda r: r['negative-syntax-test-p'] == 'False')
positive_syntax_not_parsed = positive_syntax.select(lambda r: r['parsing-succeeded-p'] == 'False')
positive_syntax_parsed = positive_syntax.select(lambda r: r['parsing-succeeded-p'] == 'True')
positive_syntax_parsed_not_translated = positive_syntax_parsed.select(lambda r: r['translation-succeeded-p'] == 'False')
positive_syntax_parsed_translated = positive_syntax_parsed.select(lambda r: r['translation-succeeded-p'] == 'True')
positive_syntax_parsed_translated_not_initialized = positive_syntax_parsed_translated.select(lambda r: r['initialization-succeeded-p'] == 'False')
positive_syntax_parsed_translated_initialized = positive_syntax_parsed_translated.select(lambda r: r['initialization-succeeded-p'] == 'True')
query = syntax.select(lambda r: r['query-evaluation-test-p'] == 'True')
query_not_runnable = query.minus(positive_syntax_parsed_translated_initialized)
query_runnable = query.intersection(positive_syntax_parsed_translated_initialized)
query_runnable_not_implemented = query_runnable.select(lambda r: r['implementedp'] != 'True')
query_runnable_implemented = query_runnable.select(lambda r: r['implementedp'] == 'True')
query_runnable_implemented_not_ran = query_runnable_implemented.select(lambda r: r['running-succeeded-p'] == 'False')
query_runnable_implemented_ran = query_runnable_implemented.select(lambda r: r['running-succeeded-p'] == 'True')
query_runnable_implemented_ran_different_semantics = query_runnable_implemented_ran.select(lambda r: r['different-semantics-p'] == 'True')
query_runnable_implemented_ran_not_compared = query_runnable_implemented.select(lambda r: r['comparing-succeeded-p'] == 'False')
query_runnable_implemented_ran_compared = query_runnable_implemented.select(lambda r: r['comparing-succeeded-p'] == 'True')
failed = allsanstimesselect(lambda r:r['failedp'] == 'True')
not_failed = allsanstimesselect(lambda r:r['failedp'] == 'False')
failed_implemented = allsanstimesselect(lambda r:r['failedp'] == 'True' and r['implementedp'] == 'True')
failed_not_implemented = allsanstimesselect(lambda r:r['failedp'] == 'True' and r['implementedp'] == 'False')

write_non_empty(suite,suite_file)
write_non_empty(suite_collection,suite_collection_file)
write_non_empty(suite_collection_double_type,suite_collection_double_type_file)
write_non_empty(not_implemented,not_implemented_file)
write_non_empty(negative_syntax_parsed,negative_syntax_parsed_file)
write_non_empty(positive_syntax_not_parsed,positive_syntax_not_parsed_file)
write_non_empty(positive_syntax_parsed_not_translated,positive_syntax_parsed_not_translated_file)
write_non_empty(positive_syntax_parsed_translated_not_initialized,positive_syntax_parsed_translated_not_initialized_file)
write_non_empty(query_not_runnable,query_not_runnable_file)
write_non_empty(query_runnable_not_implemented,query_runnable_not_implemented_file)
write_non_empty(query_runnable_implemented_not_ran,query_runnable_implemented_not_ran_file)
write_non_empty(query_runnable_implemented_ran_different_semantics,query_runnable_implemented_ran_different_semantics_file)
write_non_empty(query_runnable_implemented_ran_not_compared,query_runnable_implemented_ran_not_compared_file)
write_non_empty(failed,failed_file)
write_non_empty(failed_implemented,failed_implemented_file)
write_non_empty(failed_not_implemented,failed_not_implemented_file)

msg('\nTest suite, collection, and type statistics:')
msg('* {} tests.{}'.format(len(all), see(input_file)))
msg('* {} test suites.{}'.format(len(suite), see(suite_file)))
msg('* {} test collections.{}'.format(len(suite_collection), see(suite_collection_file)))
msg('* {} types.{}'.format(len(types), see(type_file)))
msg('* {} collections with two types.{}'.format(len(suite_collection_double_type), see(suite_collection_double_type_file)))

msg('\nTest execution statistics:')
msg('\n* {:>4} tests in total'.format(len(all)))
if len(not_implemented) > 0:
    msg('-------> {} test not executed, because features not implemented in INSTANS.{}'.format(len(not_implemented), see(not_implemented_file)))
check_counts(implemented, not_implemented, all, 6, 'tests implemented', 'tests not implemented', 'all tests', implemented_undefined_file)
if len(failed) > 0:
    msg('-------> {} tests failed.{}'.format(len(failed), see(failed_file)))
    msg('             * {} tests failed and were not implemented.{}'.format(len(failed_not_implemented), see(failed_not_implemented_file)))
    msg('-------------> {} tests failed and were implemented.{}'.format(len(failed_implemented), see(failed_implemented_file)))
msg('       * {:>3} tests succeeded.'.format(len(not_failed)))
check_counts(failed, not_failed, all, 6, 'tests failed', 'tests not failed', 'all tests', failed_undefined_file)


msg('\nSyntax test execution statistics:')
msg('\n*{:>4} syntax tests.'.format(len(syntax)))
msg('      * {} negative syntax tests.'.format(len(negative_syntax)))
if len(negative_syntax_parsed) > 0:
    msg('------------> {:>3} negative syntax tests unexpectedly parsed!{}'.format(len(negative_syntax_parsed), see(negative_syntax_parsed_file)))
msg('            * {:>3} negative syntax tests did not parse.'.format(len(negative_syntax_not_parsed)))
check_counts(negative_syntax_parsed, negative_syntax_not_parsed, negative_syntax, 12, 'negative syntax parsed ', 'negative syntax not parsed ', 'negative syntax', negative_syntax_parsed_undefined_file)

msg('      * {} positive syntax tests.'.format(len(positive_syntax)))
if len(positive_syntax_not_parsed) > 0:
    msg('-------------> {} positive syntax tests did not parse!{}'.format(len(positive_syntax_not_parsed), see(positive_syntax_not_parsed_file)))

msg('            * {} positive syntax tests parsed.'.format(len(positive_syntax_parsed)))
check_counts(positive_syntax_not_parsed, positive_syntax_parsed, positive_syntax, 12, 'positive syntax not parsed', 'positive syntax parsed', 'positive syntax', positive_syntax_parsed_undefined_file)

if len(positive_syntax_parsed_not_translated) > 0:
    msg('------------------> {:>3} positive syntax tests parsed, but did not translate!{}'.format(len(positive_syntax_parsed_not_translated), see(positive_syntax_parsed_not_translated_file)))
msg('                  * {:>3} positive syntax tests parsed and translated.'.format(len(positive_syntax_parsed_translated)))
check_counts(positive_syntax_parsed_translated, positive_syntax_parsed_not_translated, positive_syntax_parsed, 18, 'positive syntax parsed translated', 'positive syntax parsed not translated', 'positive syntax parsed', positive_syntax_parsed_translated_undefined_file)

if len(positive_syntax_parsed_translated_not_initialized) > 0:
    msg('------------------------> {:>3} positive syntax tests parsed and translated, but did not initialize!{}'.format(len(positive_syntax_parsed_translated_not_initialized), see(positive_syntax_parsed_translated_not_initialized_file)))
msg('                        * {:>3} positive syntax tests parsed, translated and initialized.'.format(len(positive_syntax_parsed_translated_initialized)))
check_counts(positive_syntax_parsed_translated_initialized, positive_syntax_parsed_translated_not_initialized, positive_syntax_parsed_translated, 24, 'positive syntax parsed translated initialized', 'positive syntax parsed translated not initialized', 'positive syntax parsed translated', positive_syntax_parsed_translated_initialized_undefined_file)

msg('\nQuery evalution test execution statistics:')
msg('\n*{:>4} query evaluation tests.'.format(len(query)))
msg('------> {:>3} query evaluation tests not runnable (not parsed, translated, or initialized)!{}'.format(len(query_not_runnable), see(query_not_runnable_file)))
msg('      * {:>3} query evaluation tests runnable (parsed, translated, initialized).'.format(len(query_runnable)))
check_counts(query_runnable, query_not_runnable, query, 6, 'query runnable', 'query not runnable', 'query', query_runnable_undefined_file)

if len(query_runnable_not_implemented) > 0:
    msg('------------> {:>3} runnable query evaluation tests with non-implemented operations in INSTANS!{}'.format(len(query_runnable_not_implemented), see(query_runnable_not_implemented_file)))
msg('            * {:>3} query_runnable evaluation tests fully implemented in INSTANS.'.format(len(query_runnable_implemented)))
check_counts(query_runnable_implemented, query_runnable_not_implemented, query_runnable, 6, 'query runnable implemented', 'query runnable not implemented', 'query runnable', query_runnable_implemented_undefined_file)

if len(query_runnable_implemented_not_ran) > 0:
    msg('------------------> {:>3} query runnable evaluation tests fully implemented in INSTANS, but dit not run!{}'.format(len(query_runnable_implemented_not_ran), see(query_runnable_implemented_not_ran_file)))
msg('                  * {:>3} query runnable evaluation tests implemented and ran.'.format(len(query_runnable_implemented_ran)))
check_counts(query_runnable_implemented_ran, query_runnable_implemented_not_ran, query_runnable_implemented, 18, 'query runnable implemented ran', 'query runnable implemented not ran', 'query runnable implemented', query_runnable_implemented_ran_undefined_file)

if len(query_runnable_implemented_ran_not_compared) > 0:
    msg('------------------------> {:>3} query runnable evaluation tests fully implemented in INSTANS, ran, but dit not compare!{}'.format(len(query_runnable_implemented_ran_not_compared), see(query_runnable_implemented_ran_not_compared_file)))
msg('                        * {:>3} query runnable evaluation tests implemented ran and compared.'.format(len(query_runnable_implemented_ran_compared)))
msg('                        * {:>3} query runnable evaluation tests implemented, ran and have different semantics.{}'.format(len(query_runnable_implemented_ran_different_semantics), see(query_runnable_implemented_ran_different_semantics_file)))
check_counts(query_runnable_implemented_ran_compared, query_runnable_implemented_ran_not_compared, query_runnable_implemented_ran, 24, 'query runnable implemented ran compared', 'query runnable implemented ran not compared', 'query runnable implemented ran', query_runnable_implemented_ran_compared_undefined_file)

msg('\nThis text is saved in {}.'.format(see(output_msgs, prefix='')))

root=os.getcwd()
msg('\nReferences')
for i in range(len(refs)):
    msg('{:>4} {}'.format('[{}]'.format(i+1), refs[i].replace(root+'/', '')))
sys.exit(0)
