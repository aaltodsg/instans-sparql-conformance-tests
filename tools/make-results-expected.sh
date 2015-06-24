#!/bin/bash
TOOLS=$(dirname $0)
cd $TOOLS/..  > /dev/null
ROOT=`pwd`

[ -f $TOOLS/result-files ] || (echo "Missing file $TOOLS/result-files"; exit 1)
ALL_FILES=( `cat $TOOLS/result-files` )

EXPECTED=$ROOT/expected
mkdir -p $EXPECTED $EXPECTED/statistics $EXPECTED/suites
if [ $# -eq 0 ]; then
    SOURCE="."
else
    SOURCE=$1
fi

STATISTICS=$SOURCE/statistics
SUITES=$SOURCE/suites

echo "Checking the existence of the directories and files:"

OK=yes
if [ ! -d $STATISTICS ]; then
    echo "  Directory $STATISTICS does not exist!"
fi
if [ ! -d $SUITES ]; then
    echo "  Directory $SUITES does not exist!"
fi

for FILE in "${ALL_FILES[@]}"; do
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

/bin/echo -n "Copy files in directory $SOURCE to directory $EXPECTED (y/n)? "
read a
[ "$a" = "y" -o "$a" = "yes" ] || (echo "Not copying"; exit 1)

for FILE in "${ALL_FILES[@]}"; do
    cp $SOURCE/$FILE $EXPECTED/$FILE
done
