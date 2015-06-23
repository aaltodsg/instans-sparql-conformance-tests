#!/bin/bash
ROOT=`(cd $(dirname $0)/..)`
STATISTICS=$ROOT/statistics
PREVSTATISTICS=$ROOT/save/latest/statistics
SUITES=$ROOT/suites
PREVSUITES=$ROOT/save/latest/suites
diff $PREVSTATISTICS/results.txt $STATISTICS/results.txt
cmp $PREVSUITES/results-sans-times.csv $SUITES/results-sans-times.csv || (echo "$PREVSUITES/results-sans-times.csv and $SUITES/results-sans-times.csv are different")




