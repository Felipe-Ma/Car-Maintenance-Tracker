from flask import Flask, render_template # Flask 

app = Flask(__name__) # Create a instance of Flask

@app.route("/")
def home():
    return "<h1> Car Maintenance Tracker </h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)