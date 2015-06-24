#!/bin/bash
TOOLS=$(dirname $0)
cd $TOOLS/..  > /dev/null
ROOT=`pwd`
[ -f $TOOLS/result-files ] || (echo "Missing file $TOOLS/result-files"; exit 1)
ALL_FILES=( `cat $TOOLS/result-files-to-copy` )
TIME=`date +%Y-%m-%dT%H:%M:%S`
SAVE=$ROOT/save/$TIME
mkdir -p $SAVE/suites $SAVE/statistics
for FILE in "${ALL_FILES[@]}"; do
    cp $FILE $SAVE/$FILE
done
tar -cvzf $ROOT/save/$TIME.tgz $ROOT/save/$TIME
rm -rf $SAVE
git add $ROOT/save/$TIME.tgz 
