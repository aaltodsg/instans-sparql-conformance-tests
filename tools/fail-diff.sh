#!/bin/bash
SEE_DIFFERENCES=$1
TOOLS=$(dirname $0)
cd $TOOLS/..  > /dev/null
ROOT=`pwd`
RESULTS=$ROOT/results
EXPECTED=$ROOT/expected

cmp_one_pair() {
    FILE1=$RESULTS/$1
    FILE2=$EXPECTED/$1
    if [ ! -f $FILE1 ]; then
	echo "Missing file $FILE1"
    elif [ ! -f $FILE2 ]; then
	echo "Missing file $FILE2"
    elif cmp -s $FILE1 $FILE2; then
	echo "OK $1"
    else
	TMP=$$_diff
	TMP1=$$_diff_1
	TMP2=$$_diff_2
	diff $FILE1 $FILE2 > $TMP
	egrep '^<' $TMP | sed '/^< /s///' > $TMP1 
	egrep '^>' $TMP | sed '/^> /s///' > $TMP2
	echo $(wc $TMP1) "tests in $FILE1 but not in $FILE2"
	if [ "$SEE_DIFFERENCES" != "" ]; then
	    cat $TMP1
	fi
	echo $(wc $TMP2) "tests in $FILE2 but not in $FILE1"
	if [ "$SEE_DIFFERENCES" != "" ]; then
	    cat $TMP2
	fi
    fi
}

for FILE in failed.csv not-failed.csv; do
    cmp_one_pair $FILE
done

