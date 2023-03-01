.PHONY: all

.EXPORT_ALL_VARIABLES:
TEXINPUTS=".:../../hpi-slides/src:./hpi-slides/src::"
TFMFONTS=".:../../hpi-slides/src:./hpi-slides/src::"
TTFONTS=".:../../hpi-slides/src:./hpi-slides/src::"


TEXSOURCES := $(wildcard *.tex)
PDFTARGETS := $(patsubst %.tex,%.pdf,$(TEXSOURCES))

# Annoying special case for ch_unterprogramme; minted in tikz: 
ablauf.pdf: callsub.pdf

all: $(PDFTARGETS)

%.pdf: %.tex
	pdflatex -shell-escape $<

clean:
	rm ${PDFTARGETS}
