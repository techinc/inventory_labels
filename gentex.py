import sys, re, simplejson as json, datetime, subprocess

def translate(dict, text):
    pattern = "(" + "|".join( re.escape(key) for key in dict.keys() ) + ")"
    regex = re.compile( pattern )
    return regex.sub( lambda mo: dict[mo.string[mo.start():mo.end()]], text )

def strip_duplicate_newlines(text):
	return '\n'.join(x for x in text.split('\n') if x != '')

def latex_escape(text):
    mapping = { u'<' : u'\\textless{}',
                u'>' : u'\\textgreater{}',
                u'~' : u'\\textasciitilde{}',
                u'&' : u'\\&',
                u'#' : u'\\#',
                u'_' : u'\\_',
                u'$' : u'\\$',
                u'%' : u'\\%',
                u'|' : u'\\docbooktolatexpipe{}',
                u'{' : u'\\{',
                u'}' : u'\\}',
                u'\n': u'\\\\',
                u'\\': u'\\textbackslash{}', }

    return translate(mapping, strip_duplicate_newlines(text))

if __name__ == '__main__':
    _, input_json, qrvector = sys.argv

    d = json.loads(''.join(file(input_json).readlines()))

    d['permissions'] = '\n'.join(d['permissions'])

    val = {}
    for k,v in d.iteritems():
        val[k] = latex_escape(v).encode('utf-8')
    qr_prog = subprocess.Popen([qrvector, '-pgf'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    qr_pgf = qr_prog.communicate(input=d['url'].encode('utf-8'))[0]

    #val['id'] = val['id'].replace("/", "/\hspace{0pt}")

    print ("""
\\documentclass{article}
\\usepackage{geometry}
\\special{papersize=60mm,50mm}
\\geometry{verbose,paperwidth=60mm,paperheight=50mm,tmargin=2mm,bmargin=2mm,lmargin=2mm,rmargin=2mm}
\\usepackage{fontspec}
\\usepackage{xunicode}
\\usepackage{xltxtra}
%\\renewcommand{\\familydefault}{\\sfdefault} 
\\usepackage{pgf}
\\usepackage[absolute]{textpos}
\\usepackage{setspace}

\\parindent=0mm

\\setlength{\TPHorizModule}{1mm}
\\setlength{\TPVertModule}{\TPHorizModule}
\\textblockorigin{2mm}{2mm}

\\begin{document}

\\begin{spacing}{.8}
\\begin{textblock}{36}[0,0](0,-4)
\\begin{center}
\\verb|chown| \\\\ \\textsf{\\textbf{"""+val['owner']+ """}} \\vspace{1mm} \\\\
\\verb|chmod| \\\\ \\textsf{\\textbf{"""+val['permissions'] + """}}
\\end{center}
\\end{textblock}
\\end{spacing}

\\begin{textblock}{18}(38,0)
\\begin{pgfpicture}{0mm}{0mm}{18mm}{18mm}
\\pgfputat{\\pgfpoint{0mm}{0mm}}{
\\begin{pgfmagnify}{1.8}{1.8} """+ qr_pgf+ """ \\end{pgfmagnify} }
\\end{pgfpicture}
\\end{textblock}

\\begin{spacing}{.8}
\\begin{textblock}{58}[.5,0](28,19)
\\begin{center}
\\textsf{\\large \\textbf{"""+val['description']+"""}}
\\vspace{1.5mm}

"""+val['comments']+"""
\\vspace{1mm}

\\textbf{"""+val['id']+"""}
\\end{center}
\\end{textblock}
\\end{spacing}

\\end{document}
""")
