TEST_RESULTS=tests/sparql-test-set/sparql-test-results.csv
INSTANS=$(INSTANS_HOME)/bin/instans
INSTANS_BIN=$(INSTANS_HOME)/bin/instans.bin

all: statistics

statistics: $(TEST_RESULTS) $(INSTANS_BIN)
	tools/test_statistics.py $(TEST_RESULTS)

$(TEST_RESULTS):
	echo "INSTANS=$(INSTANS)"
	echo "INSTANS_BIN=$(INSTANS_BIN)"
	echo "TEST_RESULTS=$(TEST_RESULTS)"
	$(INSTANS) --run-sparql-conformance-tests=$(TEST_RESULTS)

.PHONY: statistics



