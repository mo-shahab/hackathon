from unicodedata import name
from flask import Flask,render_template
app=Flask(__name__)

@app.route("/")
def func():
    
 return render_template("home.html",)
@app.route('/home')
def home():
    return f"hello i am karthik"

@app.route('/home/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)