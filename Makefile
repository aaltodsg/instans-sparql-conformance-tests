ROOT=/Users/enu/aaltodsg/sparql-conformance-tests-for-instans
SUITES=/Users/enu/aaltodsg/sparql-conformance-tests-for-instans/suites
RESULTS=/Users/enu/aaltodsg/sparql-conformance-tests-for-instans/results
INSTANS_TEST_RESULTS=$(RESULTS)/results.csv
LOG=$(RESULTS)/LOG

INSTANS_HOME=/Users/enu/aaltodsg/instans
INSTANS=$(INSTANS_HOME)/bin/instans
INSTANS_BIN=$(INSTANS_HOME)/bin/instans.bin

all: save-old instans-info results compare

full: makeinstans save-old instans-info results compare

makeinstans:
	(cd $(INSTANS_HOME); make)

save-old:
	tools/save-results.sh

instans-info:
	tools/instans-info.sh $(INSTANS_HOME) $(INSTANS) $(INSTANS_BIN) $(RESULTS)

results: $(INSTANS_TEST_RESULTS)
	tools/test_results.py $(INSTANS_TEST_RESULTS) $(RESULTS)

$(INSTANS_TEST_RESULTS): $(INSTANS_BIN)
	tools/run-tests.sh $(INSTANS) $(ROOT) $(LOG)

compare:
	tools/compare-results.sh

expected:
	tools/make-results-expected.sh

clean:
	-rm $(INSTANS_TEST_RESULTS) $(RESULTS)/*.csv

.PHONY: results force save-old makeinstans full expected compare

