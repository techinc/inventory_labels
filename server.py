from flask import Flask, render_template, request
from label import generate, printlatex

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')
    
@app.route('/print', methods=['GET','POST'])
def printlabel():
    if(request.values.get('name','') == '' or request.values.get('desc','') == ''):
        return 400
    name = request.values.get('name','')
    desc = request.values.get('desc','')
    owner = request.values.get('owner','')
    if(owner == ''):
        owner = 'TechInc'
    perms = request.values.get('perms','')
    if(perms == ''):
        perms = 'Hack it'
    latex = generate(owner, perms, name, desc)
    printlatex(latex, str(id(request)))
    return 'Label printed.'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
