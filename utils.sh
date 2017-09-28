#!/usr/bin/env bash

COMMAND="python"

if [[ $1 == "l" ]]; then
    # $2 either user or class
    fixtures=($(ls **/fixtures/*.yaml))
    for fixture in ${fixtures[@]}; do
        echo "loading $fixture"
        $COMMAND manage.py loaddata "$fixture"
    done
elif [[ $1 == "e" ]]; then
    # $2 = model to export
    # $3 = file export to
    $COMMAND manage.py dumpdata --format yaml $2 >> $3
elif [[ $1 == "mm" ]]; then
    $COMMAND manage.py makemigrations
elif [[ $1 == "m" ]]; then
    $COMMAND manage.py migrate
elif [[ $1 == "s" ]]; then
    $COMMAND manage.py runserver
elif [[ $1 == "t" ]]; then
    $COMMAND manage.py test
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
    2. e - dump currently database to file-name
        - @params 1 - models to export
        - @params 2 - file name
    3. mm - make migrations of new models
    4. m - migrate database
    5. s - run server
    6. t - test model and api
    7. r - remove currently database
    8. c - clear test-report
  "
fi
