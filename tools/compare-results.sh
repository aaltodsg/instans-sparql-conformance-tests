#!/bin/bash
ROOT=`(cd $(dirname $0)/..)`
STATISTICS=$ROOT/statistics
PREVSTATISTICS=$ROOT/save/latest/statistics
diff $PREVSTATISTICS/results.txt $STATISTICS/results.txt



