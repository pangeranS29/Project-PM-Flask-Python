from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/klasifikasi")
def klasifikasi():
    return render_template("klasifikasi.html")

if __name__ == "__main__":
    app.run(debug=True)
