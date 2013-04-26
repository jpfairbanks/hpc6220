#/usr/bin/bash
pandoc -o writeup.tex -t latex writeup.md \
       -V documentclass=IEEEtran --standalone \
       --highlight-style=pygments 
       
pdflatex writeup.tex
#evince writeup.pdf
