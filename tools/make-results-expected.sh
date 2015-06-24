#!/bin/bash
TOOLS=$(dirname $0)
cd $TOOLS/..  > /dev/null
ROOT=`pwd`

FILES_FILE=$TOOLS/result-files-to-copy
[ -f $FILES_FILE ] || (echo "Missing file $FILES_FILE"; exit 1)
ALL_FILES=( `cat $FILES_FILE` )

EXPECTED=$ROOT/expected
mkdir -p $EXPECTED
if [ $# -eq 0 ]; then
    RESULTS=results
else
    RESULTS=$1
fi

echo "Checking the existence of the directories and files:"

OK=yes
if [ ! -d $RESULTS ]; then
    echo "  Directory $RESULTS does not exist!"
fi

for NAME in "${ALL_FILES[@]}"; do
    FILE=$RESULTS/$NAME
    if [ ! -f $FILE ]; then
	echo "  $FILE is missing"
	OK=no
    else
	echo "Found $FILE"
    fi
done
if [ $OK = 'yes' ]; then
    echo "All files found"
else
    exit 1
fi

/bin/echo -n "Copy files in directory $RESULTS to directory $EXPECTED (y/n)? "
read a
[ "$a" = "y" -o "$a" = "yes" ] || (echo "Not copying"; exit 1)

for NAME in "${ALL_FILES[@]}"; do
    FILE=$RESULTS/$NAME
    cp $RESULTS/$FILE $EXPECTED/$FILE
done
