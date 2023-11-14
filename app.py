from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup app to use a SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///namedb.db'
db = SQLAlchemy(app)

# Setup a simple table for database
class Visitor(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    numVisits = db.Column(db.Integer, default=1)
    
    def __repr__(self) -> str:
        return f"{self.username} - {self.numVisits}"
    
# Create tables in database
with app.app_context():
    db.create_all()

# Function to read in details for page
def readDetails(filepath):
    with open(filepath, 'r') as f:
        return [line for line in f]
      
@app.route('/')
def homepage():
    filepath = 'static/aboutme.txt'
    text = readDetails(filepath)
    return render_template('home.html', name="Stephen's Page", aboutMe=text)

@app.route('/cheese', methods=['GET', 'POST'])
def cheesePage():
    if request.method == 'POST':
        num=request.form['num']
    try:
        int(num)
    except:
        num = False
    return render_template('cheese.html', num=int(num))

@app.route('/form', methods=['GET', 'POST'])
def formDemo():
    name = None
    if request.method == 'POST':
        name=request.form['name']
        visitor = Visitor.query.get(name)
        if visitor == None:
            visitor = Visitor(username=name)
            db.session.add(visitor)
        else:
            visitor.numVisits += 1
    db.session.commit()
    
    return render_template('form.html', name=name)

@app.route('/visitors')
def visitors():
    people = Visitor.query.all()
    return render_template('visitors.html', people=people)

if (__name__ == "__main__"):
    app.run(debug=True)