#!/usr/bin/env bash

COMMAND="python"

if [[ $1 == "l" ]]; then
    # params 2 exist
    if [ -x "$2" ]; then
        echo "load $2 fixture"
        $COMMAND manage.py loaddata "init_$2"
    else
        echo "load all"
        fixtures=($(ls **/fixtures/*.yaml))
        for fixture in ${fixtures[@]}; do
            echo "loading $fixture"
            $COMMAND manage.py loaddata "$fixture"
        done
    fi
elif [[ $1 == "e" ]]; then
    # $2 = model to export
    # $3 = file export to (optional)
    if [ -x $3 ]; then
        $COMMAND manage.py dumpdata --format yaml $2
    else
        $COMMAND manage.py dumpdata --format yaml $2 >> $3
    fi
elif [[ $1 == "mm" ]]; then
    $COMMAND manage.py makemigrations
elif [[ $1 == "m" ]]; then
    $COMMAND manage.py migrate
elif [[ $1 == "s" ]]; then
    $COMMAND manage.py runserver
elif [[ $1 == "t" ]]; then
    if [ -x $2 ]; then
        $COMMAND manage.py test
    else
        $COMMAND manage.py test $2
    fi
elif [[ $1 == "t-ci" ]]; then
    $COMMAND manage.py test --debug-sql -v 3 --testrunner xmlrunner.extra.djangotestrunner.XMLTestRunner
elif [[ $1 == "reset-database" || $1 == "reset" || $1 == "r" ]]; then
    rm -rf db.sqlite3
    echo "remove database."
elif [[ $1 == "clear-test-result" || $1 == "clear-test" || $1 == "ctr" || $1 == "c" ]]; then
    rm -rf ./test-reports/*
    echo "remove test-reports."
else
  echo "
Description: This is python utilities with django (To use this you must follow install helper in README.md)
HELP Command:
    1. l - load all fixture (test data)
        - @params 1 - (optional) fixture name (without init_*)
    2. e - dump currently database to file-name (if no file-name print as stout)
        - @params 1 - models to export
        - @params 2 - (optional) file name
    3. mm - make migrations of new models
    4. m - migrate database
    5. s - run server
    6. t - test model and api
    7. r - remove currently database
    8. c - clear test-report
  "
fi
