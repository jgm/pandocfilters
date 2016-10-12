
ALLSAMPLES = $(basename $(wildcard *-sample.md))
ALLPDF = $(addsuffix .pdf,$(ALLSAMPLES))

PYTHON=/usr/bin/python2

all: ${ALLPDF}


lilypond-sample.pdf: lilypond-sample.md
	pandoc --latex-engine lualatex --filter ./$(subst -sample.md,.py,$<) $< -o $@ || touch $@

gabc-sample.pdf: gabc-sample.md
	pandoc --latex-engine lualatex --filter ./$(subst -sample.md,.py,$<) $< -o $@ || touch $@

%.pdf: %.md
	echo $(subst -sample.md,.py,$<)
	pandoc --filter ./$(subst -sample.md,.py,$<) $< -o $@ || touch $@

clean:
	$(RM) -f ${ALLPDF} *.pyc
	$(RM) -rf *-images tmp_ly
