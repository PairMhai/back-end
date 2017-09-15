#!/usr/bin/env bash

COMMAND="python"

if [[ $1 == "load" ]]; then
    # $2 either init_class | init_admin
    $COMMAND manage.py loaddata $2
elif [[ $1 == "export" ]]; then
    # $2 = model to export
    # $3 = file export to
    $COMMAND manage.py dumpdata --format yaml $2 >> $3
elif [[ $1 == "make" ]]; then
    $COMMAND manage.py makemigrations
elif [[ $1 == "migrate" ]]; then
    $COMMAND manage.py migrate
elif [[ $1 == "server" ]]; then
    $COMMAND manage.py runserver
elif [[ $1 == "test" ]]; then
    $COMMAND manage.py test
elif [[ $1 == "clear-test-result" || $1 == "clear-test" || $1 == "ctr" ]]; then
    rm -rf ./test-reports/*
fi
