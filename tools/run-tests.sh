#!/bin/bash
INSTANS=$1
ROOT=$2
LOG=$3

${INSTANS} --run-sparql-conformance-tests=${ROOT} |  tee ${LOG}

