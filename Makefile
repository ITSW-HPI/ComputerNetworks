.PHONY: chapters chapter all slides slides169 handout clean book cleanall  quick biberclean output bibpull

# Use .SECONDARY with no argument is a little overkill, but using %.tex does not work
# because we need to refer to .tex files in subdirectories. make does not allow %/%.tex. 
.SECONDARY: 



EMACS=emacs
# typical alternatives can be something like:
# EMACS="/Applications/Emacs.app/Contents/MacOS/Emacs" 

EMACSEXPORTPARAMS= --batch -l ../templates/emacs_init.el -f org-beamer-export-to-latex

# pdflatex command
PDFLATEX=pdflatex -shell-escape -interaction=nonstopmode
BIBCOMMAND=biber


ALLSOURCES := $(wildcard *.org)
SOURCE := $(filter-out %_content.org, $(ALLSOURCES))
slidesTex := $(patsubst %.org,%.tex,$(SOURCE))
slidesPdf := $(patsubst %.org,%.pdf,$(SOURCE))
slides169Pdf := $(patsubst %.org,%_169.pdf,$(SOURCE))
handoutPdf := $(patsubst %.org,%_handout.pdf,$(SOURCE))
bookTex := $(patsubst %.org,%-chapter.tex,$(wildcard *.org))
TEMPLATES := $(wildcard ../templates/*)
BACKMATTER := ../glossary.tex
FIGURES := $(wildcard figures/*)
STANDALONEFIGS := $(wildcard standalone/*.tex)

# Setting environment for HPI slides right
.EXPORT_ALL_VARIABLES:
TEXINPUTS=".:../hpi-slides/src:./hpi-slides/src::"
TFMFONTS=".:../hpi-slides/src:./hpi-slides/src::"
TTFONTS=".:../hpi-slides/src:./hpi-slides/src::"

all:
#	-make biberclean
#	-make cleanstandalone 
	-make chapterfigures
	-make -C book book
	-make chapters

chapters:
	for d in ch*; do make -C $$d chapter  ; done

chapterfigures:
	for d in ch*; do make -C $$d/standalone all ; done 

#########################
#########################

chapter: slides handout 

quick:
	echo $$TEXINPUTS 
	quick=True make slides

slides: BEAMERPARAM = presentation,aspectratio=43
slides: OUTDIR = slides
slides: CHAPTER = $(subst .pdf,,$(slidesPdf))
slides: FILENAME = $(slidesPdf)
slides: $(slidesPdf)
	make output

handout: BEAMERPARAM = handout
handout: OUTDIR = handout
handout: CHAPTER = $(subst _handout.pdf,,$(handoutPdf))
handout: FILENAME = $(handoutPdf)
handout: $(handoutPdf)
	make output

slides169: BEAMERPARAM = presentation,aspectratio=169
slides169: OUTDIR = slides169
slides169: CHAPTER = $(subst _169.pdf,,$(slides169Pdf))
slides169: FILENAME = $(slides169Pdf)
slides169: $(slides169Pdf) 
	make output

%.tex: %.org %_content.org $(TEMPLATES) $(BACKMATTER)
	${EMACS} $< ${EMACSEXPORTPARAMS}

%_handout.tex: %.org %_content.org $(TEMPLATES) $(BACKMATTER)
	${EMACS} $< ${EMACSEXPORTPARAMS}

%_169.tex: %.org %_content.org $(TEMPLATES) $(BACKMATTER)
	${EMACS} $< ${EMACSEXPORTPARAMS}

output: DIRNUMBER = $(shell egrep -m 1 "${CHAPTER}" ../reihenfolge_kapitel.org | cut -d"." -f 1)
output:
	cp $(FILENAME) ../output/$(OUTDIR)/$(DIRNUMBER)_$(FILENAME)

%.pdf: %.tex $(STANDALONEFIGS)
	make -C standalone all 
	${PDFLATEX} "\\PassOptionsToClass{$(BEAMERPARAM)}{beamerhpi}\\input{$<}"
ifndef quick
	${BIBCOMMAND} $(basename $<)
	makeglossaries $(basename $<)
	${PDFLATEX} "\\PassOptionsToClass{$(BEAMERPARAM)}{beamerhpi}\\input{$<}"
	${PDFLATEX} "\\PassOptionsToClass{$(BEAMERPARAM)}{beamerhpi}\\input{$<}"
endif


##########################

clean:
# TODO: protect glossary.tex against being removed :-/ 
	-find . -type f -maxdepth 1 -name "*.tex" | xargs rm 
	-rm *.tex~ tmp.org *.pdf *.bbl *.vrb
	-rm -rf _minted*
	-rm *.aux *.log *.nav *.out *.snm *.toc *.pyg  *.bcf *.blg *.synctex.gz  *.fls *.fdb_latexmk *.run.xml *.auxlock
# glossary files:
	-rm *.acn *.acr *.alg *.glg *.glo *.gls *.ist

cleanall:
	make -C book clean 
	for d in ch*; do make -C $$d clean  ; done

# if biber runs crazy: 
biberclean:
	rm -rf `biber --cache`

# if there are new papers to cite:
bibpull:
	pushd ${HOME}/texmf/paperpile ; git pull ; popd 

cleanstandalone:
	find . -name "*.pdf"  | grep standalone | xargs rm
