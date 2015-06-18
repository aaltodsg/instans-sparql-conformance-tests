#!/bin/bash
ROOT=`(cd $(dirname $0)/..)`
SUITES=$ROOT/suites
STATISTICS=$ROOT/statistics
SAVE=$ROOT/save/`date +%Y-%m-%dT%H:%M:%S`
mkdir -p $SAVE/suites $SAVE/statistics
cp $SUITES/*.csv $SAVE/suites > /dev/null 2>&1
cp -a $STATISTICS $SAVE > /dev/null 2>&1
rm $ROOT/save/latest
ln -s $SAVE $ROOT/save/latest


