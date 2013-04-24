#/usr/bin/bash
pandoc -o writeup.tex -t latex writeup.md \
       -V documentclass=article --standalone \
       --highlight-style=pygments 
       
pdflatex writeup.tex
#evince writeup.pdf
