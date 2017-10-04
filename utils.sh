#!/usr/bin/env bash

COMMAND="python"

if [[ $1 == "l" ]]; then
    if [ -n "$2" ]; then
        echo "load $2 fixture"
        $COMMAND manage.py loaddata "init_$2"
    else
        echo ">> load membership and all necessary models"
        $0 l class
        $0 l user
        $0 l customer
        $0 l creditcard
        echo ">> load product and all necessary models"
        $0 l material
        $0 l design
        $0 l images
        $0 l product
        $0 l promotion
        echo ">> load mockup order and information"
        $0 l transportation
        $0 l order
        $0 l orderinfo
        echo ">> other mockup data"
        $0 l comment
        $0 l token
    fi
elif [[ $1 == "e" ]]; then
    [ -n "$2" ] || echo "models is required" && exit 1
    # $2 = model to export
    # $3 = file export to (optional)
    if [ -n "$3" ]; then
        $COMMAND manage.py dumpdata --format yaml $2 >> $3
    else
        $COMMAND manage.py dumpdata --format yaml $2
    fi
elif [[ $1 == "mm" ]]; then
    $COMMAND manage.py makemigrations
elif [[ $1 == "m" ]]; then
    $COMMAND manage.py migrate
elif [[ $1 == "s" ]]; then
    $COMMAND manage.py runserver
elif [[ $1 == "t" ]]; then
    if [ -n "$2" ]; then
        $COMMAND manage.py test $2
    else
        $COMMAND manage.py test
    fi
# heroku
elif [[ $1 == 'h' ]]; then
    which heroku &>/dev/null
    [ $? -ne 0 ] && echo "no heroku installed." && exit 1
    heroku buildpacks | grep weibeld &>/dev/null
    [ $? -ne 0 ] && heroku buildpacks:add https://github.com/weibeld/heroku-buildpack-run.git
    git remote show | grep heroku &>/dev/null
    [ $? -ne 0 ] && git remote add heroku https://git.heroku.com/pairmhai-api.git
    # deploy
    if [[ $2 == 'd' ]]; then
        # get branch in input or current branch
        [ -n "$3" ] && BRANCH="$3" || BRANCH=$(git branch | grep \* | tr '*' ' ')
        # push to master
        git push heroku $BRANCH:master
    # log
    elif [[ $2 == 'l' ]]; then
        heroku logs --tail
    fi
elif [[ $1 == "t-ci" ]]; then
    [ -d test-reports ] || mkdir test-reports
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
    1.  l    - load all fixture (test data)
               - @params 1 - (optional) fixture name (without init_*)
    2.  e    - dump currently database to file-name (if no file-name print as stout)
               - @params 1 - models to export
               - @params 2 - (optional) file name
    3.  mm   - make migrations of new models
    4.  m    - migrate database
    5.  s    - run server
    6.  h    - heroku short command
               1. d - deploy code to heroku
                      - @params 1 - (optional) branch to deploy (default is current branch)
               2. l - logs all action in heroku container
    7.  t    - test all testcase
               - @params 1 - (optional) module.testcase.method is allow to spectify test
    8.  t-ci - test all testcase with full version of debug print
    9.  r    - remove currently database
    10. c    - clear test-report
    "
fi
