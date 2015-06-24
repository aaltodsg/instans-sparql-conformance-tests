#!/bin/bash
SEE_DIFFERENCES=$1
TOOLS=$(dirname $0)
cd $TOOLS/..  > /dev/null
ROOT=`pwd`
RESULTS=$ROOT/results
EXPECTED=$ROOT/expected

FILES_FILE=$TOOLS/result-files-to-compare
[ -f $FILES_FILE ] || (echo "Missing file $FILES_FILE"; exit 1)
ALL_FILES=( `cat $FILES_FILE` )

cmp_one_pair() {
    FILE1=$RESULTS/$1
    FILE2=$EXPECTED/$1
    if [ ! -f $FILE1 ]; then
	echo "Missing file $FILE1"
    elif [ ! -f $FILE2 ]; then
	echo "Missing file $FILE2"
    elif cmp -s $FILE1 $FILE2; then
	echo "OK $1"
    elif [ "$SEE_DIFFERENCES" != "" ]; then
	/bin/echo -n "Files $FILE1 and $FILE2 are different. Want to see the differences (y/n)? "
	read a
	if [ "$a" = "y" -o  "$a" = "yes" ]; then
	    diff $FILE1 $FILE2 | less
	fi
    else
	echo "Files $FILE1 and $FILE2are different."
    fi
}

for FILE in ${ALL_FILES[@]}; do
    cmp_one_pair $FILE
done

