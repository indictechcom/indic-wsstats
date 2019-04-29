import json
from flask import Flask, render_template, url_for, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

domains = [
        'as',
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

@app.route('/wikitable')
def wikitable():

    jsonFile = open("Stats.json", "r")  # Open the JSON file for reading
    Jsondata = json.load( jsonFile )  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    Wikitable = "Statistics on "+ Jsondata[ 'timestamp']
    Wikitable += """
{|class="wikitable sortable"
|-
! colspan="7" style="text-align:center;background: #ffffff;" | Page namespace
! colspan="4" style="text-align:center;background: #ffffff;" | Main namespace
|-
!style="background: #ffffff;"|'''Language'''
!style="background: #ffffff;"|'''All pages'''
!style="background: #ddd;"|'''Without text'''
!style="background: #ffa0a0;"|'''Not proofread'''
!style="background: #b0b0ff;"|'''Problematic'''
!style="background: #ffe867;"|'''Proofread'''
!style="background: #90ff90;"|'''Validated'''
!style="background: #ffffff;"|'''All pages'''
!style="background: #90ff90;"|'''With scans'''
!style="background: #ffa0a0;"|'''Without scans'''
!style="background: #ffffff;"|'''%'''"""

    Jsondata.pop('timestamp', None)

    # Sorting
    Jsondata = json.dumps(Jsondata, sort_keys=True)
    Jsondata = json.loads( Jsondata )

    for domain in domains:

        Wikitable += """\n|-
|%s || %d || %d || %d || %d || %d || %d || %d || %d || %d || %.2f""" % (
            domain,
            Jsondata[domain]['Num_of_pages'],
            Jsondata[domain]['Without_text'],
            Jsondata[domain]['Not_proofread'],
            Jsondata[domain]['Problematic'],
            Jsondata[domain]['Proofread'],
            Jsondata[domain]['Validated'],
            Jsondata[domain]['Main_Pages'],
            Jsondata[domain]['Main_WithScan'],
            Jsondata[domain]['Main_WithOutScan'],
            100 * Jsondata[domain]["Main_WithScan"] / (Jsondata[domain]["Main_WithScan"] + Jsondata[domain]["Main_WithOutScan"])
        )

    Wikitable +="\n|}"
    return render_template('wikitable.html', Wikitable= Wikitable)

# API
@app.route('/api/stats')
def statsAPI():
    jsonFile = open("Stats.json", "r")  # Open the JSON file for reading
    Jsondata = json.load( jsonFile )  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    return jsonify( Jsondata )


@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run()
