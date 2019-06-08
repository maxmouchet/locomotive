#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

COMMAND="sncf-cli search Lyon Paris"

# "$ sncf-cli ..."
echo "\$ $COMMAND" > tmp1.txt

# sncf-cli output
$COMMAND > tmp2.txt 2>&1

cat tmp1.txt tmp2.txt > tmp.txt

carbon-now tmp.txt --config carbon.json -p default --headless
rm tmp.txt tmp1.txt tmp2.txt
