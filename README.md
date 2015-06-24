sparql-conformance-tests-for-instans
====================================

Use ./configure to set up the tests.

Use ./configure --help to see the options available. Currently there is only one option: --with-instans-home=<path-instans-home-dir>,
which should be used if ./configure cannot find INSTANS.

Run tests by make.

- 'make' or 'make all' runs the tests without first compiling your INSTANS
- 'make full' first compiles INSTANS and the runs the tests
- 'make expected' stores the current results to ./expected for later comparison
- 'make compare' compares the current and expected results. Note that 'make all' and 'make full' also run 'make compare'
- 'make clean' removes the results

