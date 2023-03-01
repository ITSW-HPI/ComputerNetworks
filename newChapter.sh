#!/bin/sh

OPTIND=1

help() {
    echo "$0 -l LectureName -c ChapterName -n ChapterNumber -r LabelForReferencing -v"
    exit 1;
}

debug() {
    echo "Lecture: " ${lecture}
    echo "Chapter Name: " ${chapterName}
    echo "Chapter Label: " ${chapterLabel}
    echo "Chapter Number: " ${chapterNumber}
    echo "Counter value: " ${counterValue}
}

# variables we want:
lecture="Computer Networks"
chapterName="Organisation"
chapterLabel="org"
chapterNumber=0
verbose=0

while getopts "hvl:c:n:r:d" opt ; do
    case "${opt}" in
	l) lecture=${OPTARG}
	   ;;
	c) chapterName=${OPTARG}
	   ;;
	n) chapterNumber=${OPTARG}
	   ;;
	r) chapterLabel=${OPTARG}
	   ;;
	h) help
	   ;;
	v) verbose=1
	   ;;
	*) help
	   ;;
    esac
done

counterValue=$(expr  $chapterNumber - 1)


if [[ $verbose -ne 0 ]]
then 
    debug
fi

echo "Creating new chapter" 

# create new directory
[[ -d ch_${chapterLabel} ]]  && { echo "Directory already exists, aborting." ; exit -1 ; }
mkdir ch_${chapterLabel}

# non-template content
pushd ch_${chapterLabel} ; ln -s ../Makefile  ; popd
mkdir ch_${chapterLabel}/figures
mkdir ch_${chapterLabel}/standalone

# org files from template
sed s/DDD/${chapterLabel}/  < templates/ch_empty/ch_empty_content.org > ch_${chapterLabel}/ch_${chapterLabel}_content.org 

sed s/AAA/"${lecture}"/ < templates/ch_empty/ch_empty.org  | \
    sed s/BBB/"${chapterName}"/ | \
    sed s/CCC/"ch_${chapterLabel}"/ | \
    sed s/DDD/"${counterValue}"/  \
    > ch_${chapterLabel}/ch_${chapterLabel}.org


# link pseudo tex files to tex file, just to have the names in place
# pushd ch_${chapterLabel} ; ln -s ch_${chapterLabel}.tex ch_${chapterLabel}_169.tex ; popd 
pushd ch_${chapterLabel} ; ln -s ch_${chapterLabel}.tex ch_${chapterLabel}_handout.tex ; popd 
pushd ch_${chapterLabel}/standalone ; ln -s ../../Makefile_standalone_figures Makefile ; popd 


# put an external document reference into templates
echo "#+LATEX_HEADER: \externaldocument{../ch_${chapterLabel}/ch_${chapterLabel}}"  >> templates/externaldocuments.org 


# modify book: create an entry to include that chapter, just before the appendix 

sed -I~  "s/* Appendix/** ${chapterName}\n\n#+include: \"..\/ch_${chapterLabel}\/ch_${chapterLabel}_content.org\"\n\n\n* Appendix/"   book/book.org

# and make sure that the graphicspaths in book point to all relevant subdirectories

echo "\\appendtographicspath{{../ch_${chapterLabel}/}}" >> book/graphicspath.tex
echo "\\appendtographicspath{{../ch_${chapterLabel}/standalone/}}" >> book/graphicspath.tex
echo "\\appendtographicspath{{../ch_${chapterLabel}/figures/}}" >> book/graphicspath.tex



