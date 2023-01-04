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

mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes  --check-untyped-defs plugins tests
# mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes --no-incremental coreinterfaces plugins tests
# mypy --config-file .mypi.ini --pretty  --show-error-codes coreinterfaces plugins tests
status=$?

echo "Exit with status: ${status}"
exit ${status}
