ROOT=/Users/enu/ttmp/instans-sparql-conformance-tests
SUITES=/Users/enu/ttmp/instans-sparql-conformance-tests/suites
INSTANS_TEST_RESULTS=$(SUITES)/results.csv
STATISTICS=/Users/enu/ttmp/instans-sparql-conformance-tests/statistics

INSTANS_HOME=/Users/enu/ttmp/instans
INSTANS=$(INSTANS_HOME)/bin/instans
INSTANS_BIN=$(INSTANS_HOME)/bin/instans.bin

all: save statistics

save:
	tools/save-results.sh

statistics: $(INSTANS_TEST_RESULTS) $(INSTANS_BIN)
	tools/test_statistics.py $(INSTANS_TEST_RESULTS) $(STATISTICS)

$(INSTANS_TEST_RESULTS):
	$(INSTANS) --run-sparql-conformance-tests=$(ROOT)

clean:
	rm $(OUTPUT_DIR)/*.csv

force: clean all

.PHONY: statistics force

