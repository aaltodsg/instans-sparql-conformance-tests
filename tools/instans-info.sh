#!/bin/bash
INSTANS_HOME=$1
INSTANS=$2
INSTANS_BIN=$3
RESULTS=$4
cd $INSTANS_HOME
{
echo =============================
echo INSTANS_HOME=$INSTANS_HOME
echo INSTANS=$INSTANS
echo INSTANS_BIN=$INSTANS_BIN
echo =============================
echo ls -l $INSTANS_BIN:
echo
ls -l $INSTANS_BIN
echo =============================
echo $INSTANS --version:
echo
$INSTANS --version
echo =============================
echo git branch:
echo
git branch
echo =============================
echo git status:
echo
git status
echo =============================
echo git log:
echo
git log
} > $RESULTS/instans.info

