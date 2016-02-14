#!/bin/sh

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <input files>"      
fi

for input in $@; do
    echo $input
    output=$(basename "${input%.*}").out
    python main.py tests/$output < $input
done
