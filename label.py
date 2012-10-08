import sys, os, re, datetime, subprocess, shutil, argparse

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
    
    return """\\documentclass{article}
\\usepackage{geometry}
\\special{papersize=60mm,50mm}
\\geometry{verbose,paperwidth=60mm,paperheight=50mm,tmargin=2mm,bmargin=2mm,lmargin=2mm,rmargin=2mm}
\\usepackage{fontspec}
\\usepackage{xunicode}
\\usepackage{xltxtra}
\\renewcommand{\\familydefault}{\\sfdefault} 
\\usepackage{pgf}
\\usepackage[absolute]{textpos}
\\usepackage{setspace}

\\parindent=0mm

\\setlength{\TPHorizModule}{1mm}
\\setlength{\TPVertModule}{\TPHorizModule}
\\textblockorigin{2mm}{2mm}

\\begin{document}

\\begin{textblock}{18}[0,0](41,26)
\\begin{picture}(1,10)
\\put(-10,-45){\includegraphics[width=18mm]{techinc.eps}}
\\end{picture}
\\end{textblock}

\\begin{spacing}{.8}
\\begin{textblock}{58}[.5,0](28,0)
\\begin{center}
\\vspace{-3mm}
\\textsf{\\large \\textbf{"""+name+"""}}
\\vspace{1.5mm}

"""+description+"""
\\vspace{1mm}

\\textbf{"""+datetime.date.today().strftime("%Y-%m-%d")+"""}
\\end{center}
\\end{textblock}
\\end{spacing}

\\begin{spacing}{.8}
\\begin{textblock}{36}[0,1](0,53)
\\verb|owner|
\\begin{center}
\\vspace{-2mm}
\\textsf{\\textbf{"""+owner+ """}} \\vspace{1mm} \\\\
\\end{center}
\\vspace{-2mm}
\\verb|permissions|
\\begin{center}
\\vspace{-2mm}
\\textsf{\\textbf{"""+permissions+ """}}
\\end{center}
\\vspace{6mm}
\\end{textblock}
\\end{spacing}

\\end{document}"""

def printlatex(latex):
    olddir = os.getcwd()
    tmp = os.environ.get("TMPDIR","/tmp/")+"label/"
    os.mkdir(tmp)
    shutil.copyfile("techinc.eps", tmp+"techinc.eps")
    os.chdir(tmp)
    with open("label.tex", "w") as f:
        f.write(latex)
    subprocess.check_call(["xelatex", "label.tex"])
    subprocess.check_call(["pdf2ps", "label.pdf", "label.ps"])
    #subprocess.check_call(["lpr", "-h", "label.ps"])
    os.chdir(olddir)
    #shutil.rmtree(tmp)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate and print labels for Technologia Incognita')
    parser.add_argument('action', choices=['gen','print'], help="[gen]erate LaTeX to stdout or [print] to send directly to printer.")
    parser.add_argument('-o', '--owner', default='TechInc', help="who the item belongs to [TechInc]")
    parser.add_argument('-p', '--perms', default='Hack it', help="what we're allowed to do with it [Hack it]")
    parser.add_argument('name', help="the name of the item")
    parser.add_argument('description', help='a description of the item')
    args = parser.parse_args()
    
    if args.action == "gen":
        latex = generate(args.owner, args.perms, args.name, args.description)
        print(latex)
    elif args.action == "print":
        latex = generate(args.owner, args.perms, args.name, args.description)
        printlatex(latex)