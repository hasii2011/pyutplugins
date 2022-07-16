#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

echo "current: $(pwd)"

mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes  core plugins tests
# mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes --no-incremental core plugins tests
# mypy --config-file .mypi.ini --pretty  --show-error-codes core plugins tests
status=$?

echo "Exit with status: ${status}"
exit ${status}
