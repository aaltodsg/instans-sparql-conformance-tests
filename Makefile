ROOT=/Users/enu/aalto-dsg/instans-sparql-conformance-tests
SUITES=/Users/enu/aalto-dsg/instans-sparql-conformance-tests/suites
INSTANS_TEST_RESULTS=$(SUITES)/results.csv
STATISTICS=/Users/enu/aalto-dsg/instans-sparql-conformance-tests/statistics
LOG=$(SUITES)/LOG

INSTANS_HOME=/Users/enu/aalto-dsg/instans
INSTANS=$(INSTANS_HOME)/bin/instans
INSTANS_BIN=$(INSTANS_HOME)/bin/instans.bin

all: save-old statistics

save-old:
	tools/save-results.sh

statistics: $(INSTANS_TEST_RESULTS)
	tools/test_statistics.py $(INSTANS_TEST_RESULTS) $(STATISTICS)

$(INSTANS_TEST_RESULTS): $(INSTANS_BIN)
	tools/run-tests.sh $(INSTANS) $(ROOT) $(LOG)

clean:
	-rm $(INSTANS_TEST_RESULTS) $(STATISTICS)/*.csv

.PHONY: statistics force save-old

