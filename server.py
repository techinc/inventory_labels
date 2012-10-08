from flask import Flask, render_template, request
from label import generate, printlatex

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')
    
@app.route('/print', methods=['POST'])
def printlabel():
    if(request.form['name'] == '' or request.form['desc'] == ''):
        return 400
    name = request.form['name']
    desc = request.form['desc']
    owner = request.form['owner']
    if(owner == ''):
        owner = 'TechInc'
    perms = request.form['perms']
    if(perms == ''):
        perms = 'Hack it'
    latex = generate(owner, perms, name, desc)
    printlatex(latex)
    return 'Label printed.'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)