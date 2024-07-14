from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/about")
def decision():
    return render_template('about.html')

app.run(debug=True)