#!/bin/bash
ROOT=`(cd $(dirname $0)/..; pwd)`
SUITES=$ROOT/suites
STATISTICS=$ROOT/statistics
SAVE=$ROOT/save/`date +%Y-%m-%dT%H:%M:%S`
mkdir -p $SAVE/suites $SAVE/statistics
cp $SUITES/*.csv $SAVE/suites
cp -a $STATISTICS $SAVE/statistics


