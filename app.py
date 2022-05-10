#import Flask
from flask import Flask, jsonify

# create app
app = Flask(__name__)

@app.route("/")
def funtion():
    print("")
    return ""

@app.route("/jsonified")
def funtion():
    print("")
    return josonify()

if __name__ == "__main__":
    app.run(debug=True)