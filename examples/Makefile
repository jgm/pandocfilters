
ALLSAMPLES = $(basename $(wildcard *-sample.md))
ALLPDF = $(addsuffix .pdf,$(ALLSAMPLES))

PYTHON=/usr/bin/python2

all: ${ALLPDF}

%.pdf: %.md
	echo $(subst -sample.md,.py,$<)
	pandoc --filter ./$(subst -sample.md,.py,$<) $< -o $@
	
clean:
	$(RM) -f ${ALLPDF} *.pyc 
	$(RM) -rf *-images
