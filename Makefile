ROOT=/Users/enu/aalto-dsg/instans-sparql-conformance-tests
SUITES=/Users/enu/aalto-dsg/instans-sparql-conformance-tests/suites
RESULTS=/Users/enu/aalto-dsg/instans-sparql-conformance-tests/results
INSTANS_TEST_RESULTS=$(RESULTS)/results.csv
LOG=$(SUITES)/LOG

INSTANS_HOME=/Users/enu/aalto-dsg/instans
INSTANS=$(INSTANS_HOME)/bin/instans
INSTANS_BIN=$(INSTANS_HOME)/bin/instans.bin

all: save-old instans-info results compare-to-prev

full: makeinstans save-old instans-info results

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

compare-to-prev:
	tools/compare-results.sh

expected:
	tools/make-results-expected.sh

clean:
	-rm $(INSTANS_TEST_RESULTS) $(RESULTS)/*.csv

.PHONY: results force save-old makeinstans full

