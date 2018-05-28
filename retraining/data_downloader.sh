#!/bin/bash

num=0
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"
    curl -o "$2/${num}.jpg" --max-time 5 $line
    num=$((num+1))
done < "$1"
