#!/bin/bash
RESTORE='\033[0m'
RED='\033[00;31m'
GREEN='\033[00;32m'
YELLOW='\e[0;33m'

HOST=18.217.156.87

export PROJ_BASE="."
CD=$(pwd)
cd $PROJ_BASE
export PROJ_BASE=$(pwd)
cd $CD

devhelp

function devhelp {
    echo -e "\t${YELLOW}Command${RESTORE}       ${YELLOW}Description${RESTORE}"
    echo -e "\t${GREEN}devhelp${RESTORE}        Prints this ${RED}help${RESTORE}"
    echo -e "\t${GREEN}buildimage${RESTORE}     ${RED}builds${RESTORE} docker image for this project"
    echo -e "\t${GREEN}sendcode${RESTORE}       ${RED}sends${RESTORE} local code to the production server"
    echo -e "\t${GREEN}redeploy${RESTORE}       ${RED}redeploys${RESTORE} the app on the production server"
}

function sendcode {
    CD=$(pwd)
    cd $PROJ_BASE
    rsync -a --progress --delete --exclude=.git . ubuntu@$HOST:./stark_skilltest
    exitcode=$?
    cd $CD
    return $exitcode
}

function buildimage {
    CD=$(pwd)
    cd $PROJ_BASE
    docker build -t integration-server .
    exitcode=$?
    cd $CD
    return $exitcode
}

function redeploy {
    sendcode
    ssh ubuntu@$HOST "cd stark_skilltest/ && docker build -t integration-server ."
    ssh ubuntu@$HOST "./dkintegration-server.sh"
    exitcode=$?
    return $exitcode
}
