pandoc -o writeup.tex -t latex writeup.md -V documentclass=IEEEtran --standalone
pdflatex writeup.tex
evince writeup.pdf
