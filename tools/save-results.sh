#!/bin/bash
TESTS=`dirname $0`/../tests
SAVE=$TESTS/save
DT=`date +%Y-%m-%dT%H:%M:%S`
mkdir -p $SAVE/$DT/input $SAVE/$DT/output
cp -a $TESTS/input $SAVE/$DT/input
cp -a $TESTS/output $SAVE/$DT/output

