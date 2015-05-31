TESTS_DIR=/Users/enu/instans/instans-sparql-conformance-tests/tests
OUTPUT_DIR=$(TESTS_DIR)/output
INSTANS_TEST_RESULTS=$(OUTPUT_DIR)/sparql-test-results.csv

INSTANS_HOME=/Users/enu/instans/instans
INSTANS=$(INSTANS_HOME)/bin/instans
INSTANS_BIN=$(INSTANS_HOME)/bin/instans.bin

all: save statistics

save:
	tools/save-results.sh

statistics: $(INSTANS_TEST_RESULTS) $(INSTANS_BIN)
	tools/test_statistics.py $(INSTANS_TEST_RESULTS)

$(INSTANS_TEST_RESULTS):
	$(INSTANS) --run-sparql-conformance-tests=$(INSTANS_TEST_RESULTS)

clean:
	rm $(OUTPUT_DIR)/*.csv

force: clean all

.PHONY: statistics force

