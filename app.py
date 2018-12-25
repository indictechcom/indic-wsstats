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
!style="background: #ffffff;"|'''%'''
    """

    Jsondata.pop('timestamp', None)

    # Sorting
    Jsondata = json.dumps(Jsondata, sort_keys=True)
    Jsondata = json.loads( Jsondata )

    for domains in Jsondata:
        Wikitable += """
|-
|%s || %d || %d || %d || %d || %d || %d || %d || %d || %d || %.2f
        """% (
            domains,
            Jsondata[domains]['Num_of_pages'],
            Jsondata[domains]['Without_text'],
            Jsondata[domains]['Not_proofread'],
            Jsondata[domains]['Problematic'],
            Jsondata[domains]['Proofread'],
            Jsondata[domains]['Validated'],
            Jsondata[domains]['Main_Pages'],
            Jsondata[domains]['Main_WithScan'],
            Jsondata[domains]['Main_WithOutScan'],
            100 * Jsondata[domains]["Main_WithScan"] / (Jsondata[domains]["Main_WithScan"] + Jsondata[domains]["Main_WithOutScan"])
        )

    Wikitable +="\n|}"
    return render_template('wikitable.html', Wikitable= Wikitable)

if __name__ == '__main__':
    app.run()
