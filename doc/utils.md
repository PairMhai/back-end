# Description:
This is python utilities with django (To use this you must follow install helper in README.md)

# HELP Command:
1.  l    - load all fixture (test data)
           - @params 1 - (optional) fixture name (without init_*)
2.  e    - dump currently database to file-name (if no file-name print as stout)
           - @params 1 - models to export
           - @params 2 - (optional) file name
3.  mm   - make migrations of new models
4.  m    - migrate database
5.  s    - run server
6.  d    - deploy code to heroku require heroku cli
           - @params 1 - (optional) branch to deploy (default is current branch)
7.  t    - test all testcase
           - @params 1 - (optional) module.TestCase.method is allow to spectify test
8.  t-ci - test all testcase with full version of debug print
9.  r    - remove currently database
10. c    - clear test-report
