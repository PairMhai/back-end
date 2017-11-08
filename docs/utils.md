# Table of Contents
- [Description](#description)
- [Global parameter](#global-parameter)
- [Feature](#feature)
- [Help Command](#help-command)
- [Example Usage](#example-usage)

# Description:
This is python utilities with django (To use this you must follow install helper in README.md)

# Global parameter:
'First Parameter' you can pass environment to the script (default=develop)
and if you pass next parameter will shift automatically in script (don't worry)
- d | dev | develop
- s | stage | staging
- p | prod | production

# Feature:
1. support multiple command separate by \",\" like '. l,mm,m develop'

# Help Command:
    # Setting
        1. setup    - setup project after you download new project down.
        2. upgrade  - upgrade library of this project.
                      - @params 1 - (optional) action after run upgrading
                        1. 'all' - upgrade all outdated library
                        2. 'x'   - dry run (don't do nothing)
        3. teardown - uninstall all library, installed by this project.
        4. sum      - summary repository and write to file 'summary-code/information.txt'

    # Develop
        1. s        - run server (default port 8000)
                      - @params 1 - (optional) port number

    # Deploy
        1. h        - heroku short command
                      1. d - deploy code to heroku (@deprecated - pull to master for update production automatically)
                           - @params 1 - (optional) branch to deploy (default is current branch)
                      2. l - logs all action in heroku container
        2. co       - collect static file

    # Database
        1. c        - check database problem
        2. mm       - make migrations of new models
        3. m        - migrate database
        4. l        - load all fixture (test data)
                      - @params 1 - (optional) fixture name (without init_*)
        5. e        - dump currently database to file-name (if no file-name print as 'stout')
                      - @params 1 - models to export
                      - @params 2 - (optional) file name

    # Testing
        1. a        - analyze using 'codeclimate'
                      - @params 1 - (optional) output format (default=html)
                      - @params 2 - (optional) output file   (default=result.html)
        2. t        - test all testcase
                      - @params 1 - (optional) module.testcase.method is allow to spectify test
        3. t-ci     - test all testcase with full debug printing and report coverage as xml
        4. cov      - report coverage with specify parameter
| - @params 1 - (optional) output type [report | html | xml] (default=report) |
| -------------------------------------------- |@params 2 - (optional) output directory (html) / file (xml)

    # Clean project
        1. r        - remove currently database
        1. d        - delete all file/folder in gitignore

# Example Usage:
1. './utils.sh s production 1234' - run server production on port 1234
2. './utils.sh h d' - deploy current branch to heroku
3. './utils.sh t membership.tests.test_login' - test all testcase in 'test_login' file
4. './utils.sh r,m,l production' - remove current database -> migrate new -> load fixture (all done by production environment)