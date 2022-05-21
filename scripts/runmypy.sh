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

mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes pyutplugincore plugins tests
# mypy --config-file .mypi.ini --pretty  --show-error-codes pyutplugincore plugins tests
status=$?

echo "Exit with status: ${status}"
exit ${status}
