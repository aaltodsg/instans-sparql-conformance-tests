#!/bin/bash
TOOLS=$(dirname $0)
cd $TOOLS/..  > /dev/null
ROOT=`pwd`
FILES_FILE=$TOOLS/result-files-to-copy
[ -f $FILES_FILE ] || (echo "Missing file $FILES_FILE"; exit 1)
ALL_FILES=( `cat $FILES_FILE` )
TIME=`date +%Y-%m-%dT%H:%M:%S`
SAVE=$ROOT/save/$TIME
mkdir -p $SAVE
for FILE in "${ALL_FILES[@]}"; do
    cp $FILE $SAVE/$FILE
done
tar -cvzf $ROOT/save/$TIME.tgz $ROOT/save/$TIME
rm -rf $SAVE
git add $ROOT/save/$TIME.tgz 
