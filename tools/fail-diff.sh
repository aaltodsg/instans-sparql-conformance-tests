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
	echo `wc -l $TMP1 | awk '{print $1}'` "tests in NEW/$1 but not in OLD/$1"
	if [ "$SEE_DIFFERENCES" != "" ]; then
	    cat $TMP1
	fi
	echo `wc -l $TMP2 | awk '{print $1}'` "tests in OLD/$1 but not in NEW/$1"
	if [ "$SEE_DIFFERENCES" != "" ]; then
	    cat $TMP2
	fi
	rm -f $TMP $TMP1 $TMP2
    fi
}

for FILE in failed.csv not-failed.csv; do
    cmp_one_pair $FILE
done

