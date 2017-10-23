#!/usr/bin/env bash

# if conda available
if command -v conda &>/dev/null; then
    conda info | grep pairmhai &>/dev/null ||\
        # shellcheck disable=SC1091
        source activate pairmhai
else
    echo "no conda"
fi

COMMAND="python"

SETTING_OPTION="--settings=Backend.settings."

get_setting() {
    if [[ "$1" == "d" || "$1" == "dev" ||  "$1" == "develop" ]]; then
        echo "${SETTING_OPTION}develop"
    elif [[ "$1" == "s" || "$1" == "stage" ||  "$1" == "staging" ]]; then
        echo "${SETTING_OPTION}staging"
    elif [[ "$1" == "p" || "$1" == "prod" ||  "$1" == "production" ]]; then
        echo "${SETTING_OPTION}production"
    else
        echo "${SETTING_OPTION}develop"
        return 1
    fi
    return 0
}

if [[ $1 == "l" ]]; then
    if setting=$(get_setting $2); then
        module="$3"
    else
        module="$2"
    fi
    if [ -n "$module" ]; then
        echo "load $module fixture"
        # echo "$COMMAND manage.py loaddata "init_$module" $s" # dry run
        $COMMAND manage.py loaddata "init_$module" $setting
    else
        echo ">> load membership and all necessary models"
        $0 l $2 class
        $0 l $2 user
        $0 l $2 customer
        $0 l $2 creditcard
        echo ">> load product and all necessary models"
        $0 l $2 material
        $0 l $2 design
        $0 l $2 images
        $0 l $2 product
        $0 l $2 promotion
        echo ">> load mockup order and information"
        $0 l $2 transportation
        $0 l $2 order
        $0 l $2 orderinfo
        echo ">> other mockup data"
        $0 l $2 comment
        $0 l $2 token
        $0 l $2 site
    fi
elif [[ $1 == "e" ]]; then
    if setting=$(get_setting $2); then
        model="$3"
        file="$4"
    else
        model="$2"
        file="$3"
    fi
    [ -n "$model" ] || echo "models is required" && exit 1
    # $2 = model to export
    # $3 = file export to (optional)
    if [ -n "$file" ]; then
        $COMMAND manage.py dumpdata --format yaml $model $setting >> $file
    else
        $COMMAND manage.py dumpdata --format yaml $model $setting
    fi
elif [[ $1 == "mm" ]]; then
    setting=$(get_setting $2)
    $COMMAND manage.py makemigrations $setting
elif [[ $1 == "m" ]]; then
    setting=$(get_setting $2)
    # echo "$COMMAND manage.py migrate $setting"; exit 155 # dry run
    $COMMAND manage.py migrate $setting
elif [[ $1 == "s" ]]; then
    setting=$(get_setting $2)
    $COMMAND manage.py runserver $setting
elif [[ $1 == "c" ]]; then
    setting=$(get_setting $2)
    # cause error
    if ! output=$(python manage.py makemigrations --check "$setting" 2>&1); then
        # merge error
        if grep merge <<< "$output" &>/dev/null; then
            echo y | $COMMAND manage.py makemigrations --merge "$setting" &&\
                echo "database need to merge. COMPLETE!"
        fi
    fi
elif [[ $1 == "t" ]]; then
    if setting=$(get_setting $2); then
        model="$3"
    else
        model="$2"
    fi
    if [ -n "$model" ]; then
        $COMMAND manage.py test "$model"
    else
        $COMMAND manage.py test
    fi
# heroku
elif [[ $1 == 'h' ]]; then
    ! command -v heroku &>/dev/null &&\
        echo "no heroku installed." &&\
        exit 1
    heroku buildpacks | grep weibeld &>/dev/null &&\
        heroku buildpacks:add https://github.com/weibeld/heroku-buildpack-run.git
    git remote show | grep heroku &>/dev/null &&\
        git remote add heroku https://git.heroku.com/pairmhai-api.git
    # deploy
    if [[ $2 == 'd' ]]; then
        # get branch in input or current branch
        [ -n "$3" ] && BRANCH="$3" || BRANCH=$(git branch | grep \* | tr '*' ' ')
        # push to master
        git push heroku "$BRANCH":master
    # log
    elif [[ $2 == 'l' ]]; then
        heroku logs --tail
    fi
elif [[ $1 == "t-ci" ]]; then
    [ -d test-reports ] || mkdir test-reports
    $COMMAND manage.py test --parallel=4 --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner --verbosity=3 --debug-sql --traceback "${SETTING_OPTION}staging"
elif [[ $1 == "reset-database" || $1 == "reset" || $1 == "r" ]]; then
    rm -rf db.sqlite3
    echo "remove database."
elif [[ $1 == "clear-test-result" || $1 == "clear-test" || $1 == "ctr" ]]; then
    rm -rf ./test-reports/*
    echo "remove test-reports."
else
    echo "
Description: This is python utilities with django (To use this you must follow install helper in README.md)
Global parameter: second parameter you can pass environment to the script (default=develop)
                  and if you pass next parameter will shift automatically in script (don't worry)
    - d | dev | develop
    - s | stage | staging
    - p | prod | production
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
               1. d - deploy code to heroku (@deprecated - pull to master for update production automatically)
                      - @params 1 - (optional) branch to deploy (default is current branch)
               2. l - logs all action in heroku container
    7.  t    - test all testcase
               - @params 1 - (optional) module.testcase.method is allow to spectify test
    8.  t-ci - test all testcase with full version of debug print
    9.  c    - check database problem
    10. r    - remove currently database
    11. ctr  - clear test-report
    "
fi
