#/usr/bin/bash
pandoc -o writeup.tex writeup.md \
       -V documentclass=IEEEtran \
       --standalone \
       --highlight-style=pygments 
       --bibliography writeup.bib 
       #--biblatex \
       #--csl IEEEtran.bst

pdflatex writeup.tex
bibtex writeup
pdflatex writeup.tex
pdflatex writeup.tex

#evince writeup.pdf
