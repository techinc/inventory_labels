import sys, re, simplejson as json, datetime, subprocess

def translate(dict, text):
    pattern = "(" + "|".join( re.escape(key) for key in dict.keys() ) + ")"
    regex = re.compile( pattern )
    return regex.sub( lambda mo: dict[mo.string[mo.start():mo.end()]], text )

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
                u'\\': u'\\textbackslash{}', }

    return translate(mapping, text)

if __name__ == '__main__':
    _, input_json, qrvector = sys.argv

    d = json.loads(''.join(file(input_json).readlines()))

    val = {}
    for k,v in d.iteritems():
        val[k] = latex_escape(v).encode('utf-8')
    qr_prog = subprocess.Popen([qrvector, '-pgf'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    qr_pgf = qr_prog.communicate(input=val['url'])[0]

    #val['id'] = val['id'].replace("/", "/\hspace{0pt}")

    print (u"""
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

\\begin{textblock}{30}[0,.5](0,12)
\\begin{center}
\\verb|chown| \\\\ \\textsf{\\large \\textbf{"""+val['owner']+ """}} \\\\ \\vspace{2mm}
\\verb|chmod| \\\\ \\textsf{\\large \\textbf{"""+val['permissions'] + """}}
\\end{center}
\\end{textblock}

\\begin{textblock}{24}(32,0)
\\begin{pgfpicture}{0mm}{0mm}{24mm}{24mm}
\\pgfputat{\\pgfpoint{0mm}{0mm}}{
\\begin{pgfmagnify}{2.4}{2.4} """+ qr_pgf+ """ \\end{pgfmagnify} }
\\end{pgfpicture}
\\end{textblock}

\\begin{textblock}{58}[.5,0](28,23)
\\begin{center}\\textsf{\\Large \\textbf{"""+val['description']+"""}}\\end{center}
\\end{textblock}

\\begin{spacing}{.8}
\\begin{textblock}{56}[.5,.5](28,37)
\\begin{center}"""+val['comments']+"""\\end{center}
\\end{textblock}
\\end{spacing}

\\begin{textblock}{58}[.5,1](28,50)
\\begin{center}\\textbf{"""+val['id']+"""}\\end{center}
\\end{textblock}

\\end{document}
""")
