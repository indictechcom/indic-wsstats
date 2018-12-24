import json
from flask import Flask, render_template, url_for

app = Flask(__name__)

domains = [
        'bn',
        'gu',
        'kn',
        'ml',
        'mr',
        'or',
        'pa',
        'sa',
        'ta',
        'te'
]

@app.route('/')
def index():
    jsonFile = open("Stats.json", "r")  # Open the JSON file for reading
    data = json.load(jsonFile)  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    return render_template('index.html', domains= domains, data= data)


if __name__ == '__main__':
    app.run(debug=True)
