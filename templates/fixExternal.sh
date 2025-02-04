#!/bin/Bash

# run this file in the templates directory!

if [[ `pwd` != *"templates" ]]; then
    echo "Run this file in the templates directory"
    exit 1
fi

find .. -name "*.tex"  | grep standalone | sed s/.tex// > "standaloneFigs.txt"

for d in `cat standaloneFigs.txt` ; do
    grep $d externaldocuments.org
    if [[ $? != 0 ]]; then
        # echo "does not exist"
        echo "#+LATEX_HEADER: \externaldocument{$d}" >> externaldocuments.org
    fi
done

