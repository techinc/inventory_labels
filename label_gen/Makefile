# Run with gmake
SHELL=/bin/sh
tex=/usr/bin/env xelatex -halt-on-error -interaction nonstopmode
python=/usr/bin/python

srcdir=.

hash=1

label_json=label_${hash}.json
label_src=label_${hash}.tex
label=label_${hash}.pdf
qrvector=${srcdir}/qrvector
gentex=${srcdir}/gentex.py

all: ${label}

${label_src}: ${qrvector} ${label_json} ${gentex}
	${python} '${gentex}' '${label_json}' '${qrvector}' > ${label_src}

${label}: ${label_src}
	${tex} ${label_src} > /dev/null 2>&1

${qrvector}: ${qrvector}.c
	gcc -std=c99 -o $@ $< -lqrencode

clean:
	-rm label_${hash}.*

