#!/usr/bin/env python3

import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from config import domains
from flask_bootstrap import Bootstrap

version = "2.0"

app = Flask(__name__)
CORS(app)
Bootstrap(app)

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

@app.route('/activeuser')
def activeuser():
    ws_project = request.args.get('project', None)
    ws_month = request.args.get('month', None)
    data = None
    total = {
        "proofread": 0,
        "validate": 0
    }
    if ws_month is not None:
        jsonFile = open("ActiveUserStats/" + ws_month + ".json", "r")
        data = json.load( jsonFile )
        jsonFile.close()
        data = data[ws_project]

        # Count the total
        for count in data.values():
            total["proofread"] = total["proofread"] + int(count["proofread"])
            total["validate"] = total["validate"] + int(count["validate"])

    return render_template('activeuser.html', data= data, project=ws_project, total=total)

if __name__ == '__main__':
    app.run()
