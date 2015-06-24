ROOT=/Users/enu/aalto-dsg/aux/instans-sparql-conformance-tests
SUITES=/Users/enu/aalto-dsg/aux/instans-sparql-conformance-tests/suites
INSTANS_TEST_RESULTS=$(SUITES)/results.csv
STATISTICS=/Users/enu/aalto-dsg/aux/instans-sparql-conformance-tests/statistics
LOG=$(SUITES)/LOG

INSTANS_HOME=../instans
INSTANS=$(INSTANS_HOME)/bin/instans
INSTANS_BIN=$(INSTANS_HOME)/bin/instans.bin

all: save-old instans-info statistics compare-to-prev

full: makeinstans save-old instans-info statistics

makeinstans:
	(cd $(INSTANS_HOME); make)

save-old:
	tools/save-results.sh

instans-info:
	tools/instans-info.sh $(INSTANS_HOME) $(INSTANS) $(INSTANS_BIN) $(STATISTICS)

statistics: $(INSTANS_TEST_RESULTS)
	tools/test_statistics.py $(INSTANS_TEST_RESULTS) $(STATISTICS)

$(INSTANS_TEST_RESULTS): $(INSTANS_BIN)
	tools/run-tests.sh $(INSTANS) $(ROOT) $(LOG)

compare-to-prev:
	tools/compare-results.sh

clean:
	-rm $(INSTANS_TEST_RESULTS) $(STATISTICS)/*.csv

.PHONY: statistics force save-old makeinstans full

