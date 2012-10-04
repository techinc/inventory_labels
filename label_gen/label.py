import sys, re, datetime, subprocess

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
    
def generate(owner, permissions, name, description):

    owner = latex_escape(owner).encode('utf-8')
    permissions = latex_escape(permissions).encode('utf-8')
    name = latex_escape(name).encode('utf-8')
    description = latex_escape(description).encode('utf-8')

    f = open("logo.pgf")
    logo = f.read()
    f.close()
    
    return """
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
\\verb|owner| \\\\ \\textsf{\\textbf{"""+owner+ """}} \\vspace{1mm} \\\\
\\verb|permissions| \\\\ \\textsf{\\textbf{"""+permissions+ """}}
\\end{center}
\\end{textblock}
\\end{spacing}

\\begin{textblock}{18}(38,0)
\\begin{pgfpicture}{0mm}{0mm}{18mm}{18mm}
\\pgfputat{\\pgfpoint{0mm}{0mm}}{
\\begin{pgfmagnify}{1.8}{1.8} """+logo+ """ \\end{pgfmagnify} }
\\end{pgfpicture}
\\end{textblock}

\\begin{spacing}{.8}
\\begin{textblock}{58}[.5,0](28,19)
\\begin{center}
\\textsf{\\large \\textbf{"""+name+"""}}
\\vspace{1.5mm}

"""+description+"""
\\vspace{1mm}

\\textbf{"""+datetime.date.today().strftime("%d-%m-%y")+"""}
\\end{center}
\\end{textblock}
\\end{spacing}

\\end{document}
"""

if __name__ == '__main__':
    _, file, owner, permissions, name, description = sys.argv

    latex = generate(owner, permissions, name, description)
    f = open(file, "w")
    f.write(latex)
    f.close()