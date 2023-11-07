from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def homepage():
    filepath = 'static/aboutme.txt'
    with open(filepath, 'r') as f:
        text = [line for line in f]
    return render_template('template.html', name="Stephen's Page", aboutMe=text)

@app.route('/cheese', methods=['GET', 'POST'])
def formDemo():
    if request.method == 'POST':
        num=request.form['num']
    try:
        int(num)
    except:
        num = False
    return render_template('form.html', num=int(num))



if (__name__ == "__main__"):
    app.run(debug=True)