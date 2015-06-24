#!/bin/bash
SEE_DIFFERENCES=$1
TOOLS=$(dirname $0)
cd $TOOLS/..  > /dev/null
ROOT=`pwd`
EXPECTED=$ROOT/expected
[ -f $TOOLS/result-files ] || (echo "Missing file $TOOLS/result-files"; exit 1)
ALL_FILES=( `cat $TOOLS/result-files-to-compare` )

cmp_one_pair() {
    if cmp -s $ROOT/$1 $EXPECTED/$1; then
	echo "OK $1"
    elif [ "$SEE_DIFFERENCES" != "" ]; then
	/bin/echo -n "Files $ROOT/$1 and $EXPECTED/$1 are different. Want to see the differences (y/n)? "
	read a
	if [ "$a" = "y" -o  "$a" = "yes" ]; then
	    diff $ROOT/$1 $EXPECTED/$1 | less
	fi
    else
	echo "Files $ROOT/$1 and $EXPECTED/$1 are different."
    fi
}

for FILE in ${ALL_FILES[@]}; do
    cmp_one_pair $FILE
done

