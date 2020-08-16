#!/usr/bin/env sh

inputs="$(xinput list | egrep -i 'Mouse|Keyboard|Touch' | egrep -o 'id=\S*\s' | egrep -o '[0-9]*')"
# echo "$inputs"
for input in $inputs; do
    xinput disable $input
done
sleep "$1"
for input in $inputs; do
    xinput enable "$input"
done
