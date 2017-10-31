#!/usr/bin/env bash

# setup project
if [[ $1 == "setup" ]]; then
    ! command -v conda &>/dev/null && echo "conda required to setup project!" && exit 1

    echo ">> install conda dependencies."
    conda create --name pairmhai --file requirements_conda.txt

    echo ">> install dependencies."
    pip install -r requirements.txt

    exit 0
fi

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

### EXTRA FEATURE!
#### format ./utils.sh r,mm,m,l [develop|production]
if [[ $1 =~ "," ]]; then
    IFS=',' read -r -a arr <<< "$1"
    shift
    for i in "${arr[@]}"; do
        echo "run $i -->"
        $0 $i $@
        echo "--> END!"
    done
    exit $?
fi

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

# ---------------------------------
# function section
# ---------------------------------

load() {
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
        $0 l $2 email
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
}

export_database() {
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
}

make_migrate() {
    setting=$(get_setting $2)
    $COMMAND manage.py makemigrations $setting
}

migrate() {
    setting=$(get_setting $2)
    # echo "$COMMAND manage.py migrate $setting"; exit 155 # dry run
    $COMMAND manage.py migrate $setting
}

run_server() {
    setting=$(get_setting $2)
    if setting=$(get_setting $2); then
        port="$3"
    else
        port="$2"
    fi
    $COMMAND manage.py runserver $setting $port
}

check() {
    setting=$(get_setting $2)
    # cause error
    if ! output=$(python manage.py makemigrations --check "$setting" 2>&1); then
        # merge error
        if grep merge <<< "$output" &>/dev/null; then
            echo y | $COMMAND manage.py makemigrations --merge "$setting" &&\
                echo "database need to merge. COMPLETE!"
        fi
    fi
}

collect() {
    setting=$(get_setting $2)
    $COMMAND manage.py collectstatic $setting
}

test_py() {
    if setting=$(get_setting $2); then
        model="$3"
    else
        model="$2"
    fi

    if [ -n "$model" ]; then
        $COMMAND manage.py test $setting "$model"
    else
        $COMMAND manage.py test $setting
    fi
}

coverage_py() {
    ! command -v coverage &>/dev/null && echo "coverage required to run coverage!" && exit 1

    if setting=$(get_setting $2); then
        model="$3"
    else
        model="$2"
    fi

    if [ -n "$model" ]; then
        coverage run --source='.' manage.py test $setting "$model"
        coverage report
    else
        coverage run --source='.' manage.py test $setting
        coverage report
    fi
}

test_ci() {
    ! command -v coverage &>/dev/null && echo "coverage required to run coverage!" && exit 1
    [ -d test-reports ] || mkdir test-reports

    coverage run --source='.' manage.py test --parallel=4 --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner --verbosity=3 --debug-sql --traceback "${SETTING_OPTION}staging"
    # coverage report
    coverage xml
}

heroku_deploy() {
    [ -n "$3" ] && BRANCH="$3" || BRANCH=$(git branch | grep \* | tr '*' ' ')
    git push heroku "${BRANCH// /}":master # push to master
}

heroku_log() {
    heroku logs --tail
}

heroku_imp() {
    ! command -v heroku &>/dev/null &&\
        echo "no heroku installed." &&\
        exit 1
    heroku buildpacks | grep weibeld &>/dev/null ||\
        heroku buildpacks:add https://github.com/weibeld/heroku-buildpack-run.git
    git remote show | grep heroku &>/dev/null ||\
        git remote add heroku https://git.heroku.com/pairmhai-api.git

    [[ $2 == 'd' ]] && heroku_deploy   && exit 0
    [[ $2 == 'l' ]] && heroku_log      && exit 0
}

remove_db() {
    [ -f db.sqlite3 ] && echo "remove database."
    rm -rf db.sqlite3
}

remove_all() {
    [ -d test-reports ] && echo "remove report."
    rm -rf ./test-reports/*

    [ -d static ] && echo "remove static."
    rm -rf ./static/*

    [ -f .coverage ] && echo "remove coverage."
    rm -rf *coverage*
}

summary_code() {
    echo "# $(date)" > ./summary-code/information.txt
    git-summary >> ./summary-code/information.txt
}

# ---------------------------------
# parameter section
# ---------------------------------

[[ $1 == "l" ]]     && load $@            && exit 0
[[ $1 == "e" ]]     && export_database $@ && exit 0
[[ $1 == "mm" ]]    && make_migrate $@    && exit 0
[[ $1 == "m" ]]     && migrate $@         && exit 0
[[ $1 == "s" ]]     && run_server $@      && exit 0
[[ $1 == "c" ]]     && check $@           && exit 0
[[ $1 == "co" ]]    && collect $@         && exit 0
[[ $1 == "cov" ]]   && coverage_py $@     && exit 0
[[ $1 == "t" ]]     && test_py $@         && exit 0
[[ $1 == "t-ci" ]]  && test_ci $@         && exit 0
[[ $1 == "h" ]]     && heroku_imp $@      && exit 0
[[ $1 == "r" ]]     && remove_db $@       && exit 0
[[ $1 == "d" ]]     && remove_all $@      && exit 0
[[ $1 == "sum" ]]   && summary_code $@    && exit 0


echo "
Description:
    This is python utilities with django (To use this you must follow install helper in README.md)

Global parameter:
    'First Parameter' you can pass environment to the script (default=develop)
    and if you pass next parameter will shift automatically in script (don't worry)
    - d | dev | develop
    - s | stage | staging
    - p | prod | production

Feature:
1. support multiple command separate by "," like '. l,mm,m develop'

Help Command:
    # Setting
        1. setup   - setup project after you download new project down.
        2. sum     - summary repository and write to file 'summary-code/information.txt'

    # Develop
        1. s       - run server (default port 8000)
                     - @params 1 - (optional) port number

    # Deploy
        1. h       - heroku short command
                     1. d - deploy code to heroku (@deprecated - pull to master for update production automatically)
                          - @params 1 - (optional) branch to deploy (default is current branch)
                     2. l - logs all action in heroku container
        2. co      - collect static file

    # Database
        1. c       - check database problem
        2. mm      - make migrations of new models
        3. m       - migrate database
        4. l       - load all fixture (test data)
                     - @params 1 - (optional) fixture name (without init_*)
        5. e       - dump currently database to file-name (if no file-name print as 'stout')
                     - @params 1 - models to export
                     - @params 2 - (optional) file name

    # Testing
        1. t       - test all testcase
                     - @params 1 - (optional) module.testcase.method is allow to spectify test
        2. cov     - coverage test and report to 'stdout'
                     - @params 1 - (optional) module.testcase.method is allow to spectify test
        3. t-ci    - test all testcase with full debug printing

    # Clean project
        1. r       - remove currently database
        1. d       - delete all file/folder in gitignore

Example Usage:
1. './utils.sh s production 1234' - run server production on port 1234
2. './utils.sh h d' - deploy current branch to heroku
3. './utils.sh t membership.tests.test_login' - test all testcase in 'test_login' file
4. './utils.sh r,m,l production' - remove current database -> migrate new -> load fixture (all done by production environment)
    "
