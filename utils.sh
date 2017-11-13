#!/usr/bin/env bash
# shellcheck disable=SC2063,SC1091,SC2068

# setup project
if [[ $1 == "setup" ]]; then
    ! command -v conda &>/dev/null && echo "conda required to setup project!" && exit 1

    if [ $(conda info --envs | grep pairmhai -q) ]; then
        source activate pairmhai
    else
        conda create --name pairmhai --file requirements_conda.txt
        echo ">> install conda dependencies."
        source activate pairmhai
    fi

    echo ">> install dependencies."
    pip install -r requirements.txt
    exit 0
fi

# if conda available
if command -v conda &>/dev/null; then
    conda info | grep pairmhai &>/dev/null ||
        # shellcheck disable=SC1091
        source activate pairmhai
else
    echo "no conda"
fi

# upgrade project
if [[ $1 == "upgrade" ]]; then
    source activate pairmhai
    echo ">> upgrade dependencies."
    echo "$2" | pip-upgrade --skip-package-installation requirements.txt
    exit 0
fi

# uninstall project
if [[ $1 == "teardown" ]]; then
    app=($(\cat requirements.txt | tr '\n' ' ')) # list of app
    for a in ${app[@]}; do
        echo "y" | pip uninstall "${a%%==*}"
    done
    exit 0
fi

COMMAND="python"

SETTING_OPTION="--settings=Backend.settings."

export source="Backend,cart,catalog,comment,landingpage,membership,payment,utilities,version"

### EXTRA FEATURE!
#### format ./utils.sh r,mm,m,l [develop|production]
if [[ $1 =~ , ]]; then
    IFS=',' read -r -a arr <<<"$1"
    shift
    for i in "${arr[@]}"; do
        echo "run $i -->"
        $0 "$i" "$@"
        echo "--> END!"
    done
    exit $?
fi

get_setting_name() {
    if [[ $1 == "d" || $1 == "dev" || $1 == "develop" ]]; then
        echo "develop"
    elif [[ $1 == "s" || $1 == "stage" || $1 == "staging" ]]; then
        echo "staging"
    elif [[ $1 == "p" || $1 == "prod" || $1 == "production" ]]; then
        echo "production"
    else
        echo "develop"
        return 1
    fi
    return 0
}

get_setting() {
    local name
    name="$(get_setting_name "$1")"
    exit_code="$?"
    echo "${SETTING_OPTION}$name"
    return $exit_code
}

# ---------------------------------
# function section
# ---------------------------------

load() {
    if setting=$(get_setting "$2"); then
        module="$3"
    else
        module="$2"
    fi
    if [ -n "$module" ]; then
        echo "load $module fixture"
        # echo "$COMMAND manage.py loaddata "init_$module" $s" # dry run
        $COMMAND manage.py loaddata "init_$module" "$setting"
    else
        echo ">> load membership and all necessary models"
        $0 l "$(get_setting_name "$2")" class
        $0 l "$(get_setting_name "$2")" user
        $0 l "$(get_setting_name "$2")" email
        $0 l "$(get_setting_name "$2")" customer
        $0 l "$(get_setting_name "$2")" creditcard
        echo ">> load product and all necessary models"
        $0 l "$(get_setting_name "$2")" material
        $0 l "$(get_setting_name "$2")" design
        $0 l "$(get_setting_name "$2")" images
        $0 l "$(get_setting_name "$2")" product
        $0 l "$(get_setting_name "$2")" promotion
        echo ">> load mockup order and information"
        $0 l "$(get_setting_name "$2")" transportation
        $0 l "$(get_setting_name "$2")" order
        $0 l "$(get_setting_name "$2")" orderinfo
        echo ">> other mockup data"
        $0 l "$(get_setting_name "$2")" comment
        $0 l "$(get_setting_name "$2")" token
        $0 l "$(get_setting_name "$2")" site
    fi
}

export_database() {
    if setting=$(get_setting "$2"); then
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
        $COMMAND manage.py dumpdata --format yaml "$model" "$setting" >>"$file"
    else
        $COMMAND manage.py dumpdata --format yaml "$model" "$setting"
    fi
}

make_migrate() {
    setting=$(get_setting "$2")
    $COMMAND manage.py makemigrations "$setting"
}

migrate() {
    setting=$(get_setting "$2")
    # echo "$COMMAND manage.py migrate "$setting""; exit 155 # dry run
    $COMMAND manage.py migrate "$setting"
}

run_server() {
    if setting=$(get_setting "$2"); then
        port="$3"
    else
        port="$2"
    fi
    $COMMAND manage.py runserver "$setting" "$port"
}

check() {
    setting=$(get_setting "$2")
    # cause error
    if ! output=$(python manage.py makemigrations --check "$setting" 2>&1); then
        # merge error
        if grep merge <<<"$output" &>/dev/null; then
            echo y | $COMMAND manage.py makemigrations --merge "$setting" &&
                echo "database need to merge. COMPLETE!"
        fi
    fi
}

collect() {
    setting=$(get_setting "$2")
    $COMMAND manage.py collectstatic "$setting"
}

test_py() {
    if setting=$(get_setting "$2"); then
        model="$3"
    else
        model="$2"
    fi

    if [ -n "$model" ]; then
        coverage run --source="$source" manage.py test "$setting" "$model"
    else
        coverage run --source="$source" manage.py test "$setting"
    fi
}

coverage_py() {
    ! command -v coverage &>/dev/null && echo "coverage required to run coverage!" && exit 1

    type="report"
    [ -n "$2" ] && type="$2"

    [[ $type != "report" ]] && directory="$3"

    [[ $type == "xml" ]] && [ -n "$directory" ] && result_file="-o $directory"
    [[ $type == "html" ]] && [ -n "$directory" ] && result_file="--directory=$directory"

    coverage $type $result_file
}

test_ci() {
    ! command -v coverage &>/dev/null && echo "coverage required to run coverage!" && exit 1
    [ -d test-reports ] || mkdir test-reports
    setting=$(get_setting "$2")

    [[ $setting =~ develop ]] && setting="${SETTING_OPTION}staging" # on ci test, cannot set env to develop

    echo "
############################################################
    run:
    coverage run
        --source=$source
        manage.py test
        --parallel=4
        --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner
        --verbosity=3
        --debug-sql
        $setting
############################################################
"
    coverage run \
        --source=$source \
        manage.py test \
        --parallel=4 \
        --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner \
        --verbosity=3 \
        --debug-sql \
        "$setting"
    [ $? -eq 0 ] && coverage xml # coverage report (run only test True)
}

heroku_deploy() {
    [ -n "$3" ] && BRANCH="$3" || BRANCH=$(git branch | grep \* | tr '*' ' ')
    git push heroku "${BRANCH// /}":master # push to master
}

heroku_log() {
    heroku logs --tail
}

heroku_imp() {
    ! command -v heroku &>/dev/null &&
        echo "no heroku installed." &&
        exit 1
    heroku buildpacks | grep weibeld &>/dev/null ||
        heroku buildpacks:add https://github.com/weibeld/heroku-buildpack-run.git
    git remote show | grep heroku &>/dev/null ||
        git remote add heroku https://git.heroku.com/pairmhai-api.git

    [[ $2 == 'd' ]] && heroku_deploy "$@" && exit 0
    [[ $2 == 'l' ]] && heroku_log && exit 0
}

remove_db() {
    [ -f db.sqlite3 ] && echo "remove database."
    rm -rf db.sqlite3
}

remove_all() {
    rm -r ./test-reports/* 2>/dev/null && echo "remove report."
    rm -r ./static/* 2>/dev/null && echo "remove static."
    rm -r .coverage* 2>/dev/null && echo "remove .coverage*."
    rm -r coverage* 2>/dev/null && echo "remove coverage*."
    rm -r *htmlcov* 2>/dev/null && echo "remove htmlcov."
    return 0
}

summary_code() {
    echo "# $(date)" >./summary-code/information.txt
    git-summary >>./summary-code/information.txt
}

analyze() {
    ! command -v codeclimate &>/dev/null &&
        echo "no codeclimate installed." &&
        exit 1

    format="$2"
    file="$3"
    [ -z "$2" ] && format="html"
    [ -z "$3" ] && file="result.html"

    codeclimate analyze -f "$format" >"$file"
}

release() {
    printf "update to => dev=%s       \n" "$2"
    printf "          => pro=%s [Y|n] " "$3"
    read -rn 1 ans
    if [[ "$ans" == "y" ]] || [[ "$ans" == "Y" ]]; then
        DUMP=":bookmark: Dump version: $3"
        IMPORT="from .base import *"
        D_VERSION="VERSION = \"$2-beta.1\""
        S_VERSION="VERSION = \"$3-test.1\""
        P_VERSION="VERSION = \"$3\""

        echo "run..."
        echo "developing..."
        printf "%s\n\n" "$IMPORT" > ./Backend/settings/develop.py
        printf "%s\n\n" "$D_VERSION" >> ./Backend/settings/develop.py
        cat ./Backend/settings/temp/dtemp.py >> ./Backend/settings/develop.py

        echo "staging..."
        printf "%s\n\n" "$IMPORT" > ./Backend/settings/staging.py
        printf "%s\n\n" "$S_VERSION" >> ./Backend/settings/staging.py
        cat ./Backend/settings/temp/stemp.py >> ./Backend/settings/staging.py

        echo "producting..."
        printf "%s\n\n" "$IMPORT" > ./Backend/settings/production.py
        printf "%s\n\n" "$P_VERSION" >> ./Backend/settings/production.py
        cat ./Backend/settings/temp/ptemp.py >> ./Backend/settings/production.py

        echo "creating changelog..."
        git changelog --no-merges --tag "$3"

        echo "git adding..."
        git add .
        echo "git committing..."
        git commit -am "$DUMP"
        echo "git tagging..."
        git tag "$3"
        echo "git pushing..."
        git push
        git push --tag
    else
        echo "stop!"
    fi
}

help() {
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
1. support multiple command separate by \",\" like '. l,mm,m develop'

Help Command:
    # Setting
        1. setup    - setup project after you download new project down.
        2. upgrade  - upgrade library of this project.
                      - @params 1 - (optional) action after run upgrading
                        1. 'all' - upgrade all outdated library
                        2. 'x'   - dry run (don't do nothing)
        3. teardown - uninstall all library, installed by this project.
        4. summary  - summary repository and write to file 'summary-code/information.txt'

    # Develop
        1. s        - run server (default port 8000)
                      - @params 1 - (optional) port number

    # Deploy
        1. h        - heroku short command
                      1. d - deploy code to heroku (@deprecated - pull to master for update production automatically)
                           - @params 1 - (optional) branch to deploy (default is current branch)
                      2. l - logs all action in heroku container
        2. co       - collect static file
        3. v        - release new version
                      - @param 1 - text of develop version
                      - @param 2 - text of staging and production version in git tag

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
                      - @params 1 - (optional) output type [report|html|xml] (default=report)
                      - @params 2 - (optional) output directory (html) / file (xml)

    # Clean project
        1. r        - remove currently database
        1. d        - delete all file/folder in gitignore

Example Usage:
1. './utils.sh s production 1234' - run server production on port 1234
2. './utils.sh h d' - deploy current branch to heroku
3. './utils.sh t membership.tests.test_login' - test all testcase in 'test_login' file
4. './utils.sh r,m,l production' - remove current database -> migrate new -> load fixture (all done by production environment)
    "
}

# ---------------------------------
# parameter section
# ---------------------------------

[[ $1 == "a" ]]       && analyze "$@"         && exit 0
[[ $1 == "e" ]]       && export_database "$@" && exit 0
[[ $1 == "l" ]]       && load "$@"            && exit 0
[[ $1 == "mm" ]]      && make_migrate "$@"    && exit 0
[[ $1 == "m" ]]       && migrate "$@"         && exit 0
[[ $1 == "s" ]]       && run_server "$@"      && exit 0
[[ $1 == "c" ]]       && check "$@"           && exit 0
[[ $1 == "co" ]]      && collect "$@"         && exit 0
[[ $1 == "cov" ]]     && coverage_py "$@"     && exit 0
[[ $1 == "d" ]]       && remove_all "$@"      && exit 0
[[ $1 == "t-ci" ]]    && test_ci "$@"         && exit 0
[[ $1 == "t" ]]       && test_py "$@"         && exit 0
[[ $1 == "h" ]]       && heroku_imp "$@"      && exit 0
[[ $1 == "r" ]]       && remove_db "$@"       && exit 0
[[ $1 == "summary" ]] && summary_code "$@"    && exit 0
[[ $1 == "v" ]]       && release "$@"         && exit 0

[[ $1 == "h" ]]       && help && exit 0
[[ $1 == "-h" ]]      && help && exit 0
[[ $1 == "help" ]]    && help && exit 0
[[ $1 == "-help" ]]   && help && exit 0
[[ $1 == "--help" ]]  && help && exit 0
