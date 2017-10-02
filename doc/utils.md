# Description: 
This is python utilities with django (To use this you must follow install helper in README.md)

# HELP Command:
1. l    - load all fixture (test data)
          - @params 1 - (optional) fixture name (without init_*)
2. e    - dump currently database to file-name (if no file-name print as stout)
          - @params 1 - models to export
          - @params 2 - (optional) file name
3. mm   - make migrations of new models
4. m    - migrate database
5. s    - run server
6. t    - test all testcase
          - @params 1 - (optional) module.TestCase.method is allow to spectify test
7. t-ci - test all testcase with full version of debug print
7. r    - remove currently database
8. c    - clear test-report
