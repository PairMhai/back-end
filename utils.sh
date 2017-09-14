#!/usr/bin/env bash

if [[ $1 == "load" ]]; then
    python manage.py loaddata $2
elif [[ $1 == "export" ]]; then
    # $2 = model to export
    # $3 = file export to
    python manage.py dumpdata --format yaml $2 >> $3
elif [[ $1 == "server" ]]; then
    python manage.py runserver
fi
