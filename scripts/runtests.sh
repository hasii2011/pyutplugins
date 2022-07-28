#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi

    if [[ ${areHere} = "src" ]]; then
        cd ..
    fi
}

function checkStatus {

    status=$1
    testName=$2

    echo "checkStatus ${testName} -- ${status}"
    if [ "${status}" -ne 0 ]
    then
        exit "${status}"
    fi
}

changeToProjectRoot

echo "Travis Build directory: ${TRAVIS_BUILD_DIR}"
# shellcheck disable=SC2164
cd src > /dev/null 2>&1
echo "current: $(pwd)"

python3 -m tests.TestAll "$*"
status=$?

cd -  > /dev/null 2>&1 || exit

echo "Exit with status: ${status}"
exit "${status}"

