#!/bin/bash
TOOLS=$(dirname $0)
cd $TOOLS/..  > /dev/null
ROOT=`pwd`
EXPECTED=$ROOT/expected
STATISTICS=$ROOT/statistics
EXPECTEDSTATISTICS=$EXPECTED/statistics
SUITES=$ROOT/suites
EXPECTEDSUITES=$EXPECTED/suites
diff $EXPECTEDSTATISTICS/results.txt $STATISTICS/results.txt
if cmp $EXPECTEDSUITES/results-sans-times.csv $SUITES/results-sans-times.csv; then
    echo "Got the expected results"
else
    echo "$EXPECTEDSUITES/results-sans-times.csv and $SUITES/results-sans-times.csv are different"
    /bin/echo -n "Want to compare (y/n)? "
    read a
    if [ "$a" = "y" -o "$a" = "yes" ]; then
	diff  $EXPECTEDSUITES/results-sans-times.csv $SUITES/results-sans-times.csv | less
    fi
fi




