#!/usr/bin/env python3

import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from config import domains

__version__ = "2.0"

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    with open ("Stats.json","r") as st:
        data = json.load(st)  # Open the JSON file for reading
      
    return render_template('index.html', domains= domains, data= data)

@app.route('/wikitable')
def wikitable():

    with open ("Stats.json","r") as st:
        jsonData = json.load(st) # Open the JSON file for reading

    wikiTable = "Statistics on "+ jsonData[ 'timestamp']
    wikiTable += """
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

    jsonData.pop('timestamp', None)

    # Sorting
    jsonData = json.dumps(jsonData, sort_keys=True)
    jsonData = json.loads( jsonData )

    for domain in domains:

        wikiTable += """\n|-
|%s || %d || %d || %d || %d || %d || %d || %d || %d || %d || %.2f""" % (
            domain,
            jsonData[domain]['Num_of_pages'],
            jsonData[domain]['Without_text'],
            jsonData[domain]['Not_proofread'],
            jsonData[domain]['Problematic'],
            jsonData[domain]['Proofread'],
            jsonData[domain]['Validated'],
            jsonData[domain]['Main_Pages'],
            jsonData[domain]['Main_WithScan'],
            jsonData[domain]['Main_WithOutScan'],
            100 * jsonData[domain]["Main_WithScan"] / (jsonData[domain]["Main_WithScan"] + jsonData[domain]["Main_WithOutScan"])
        )

    wikiTable +="\n|}"
    return render_template('wikitable.html', Wikitable= wikiTable)

# API
@app.route('/api/stats')
def statsAPI():
    with open ("Stats.json","r") as st:
        jsonData = json.load(st)  # Open the JSON file for reading

    return jsonify( jsonData )


@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/activeuser')
def activeuser():
    wsProject = request.args.get('project', None)
    wsMonth = request.args.get('month', None)
    data = None
    fileExists = True
    total = {
        "proofread": 0,
        "validate": 0
    }
    if wsMonth is not None:
        try:
            jsonFile = open("ActiveUserStats/" + wsMonth + ".json", "r")
            data = json.load( jsonFile )
            jsonFile.close()
            data = data[wsProject]

            # Count the total
            for count in data.values():
                total["proofread"] = total["proofread"] + int(count["proofread"])
                total["validate"] = total["validate"] + int(count["validate"])
            return render_template('activeuser.html', data= data, project=wsProject, total=total, fileExists=True)
        except FileNotFoundError:
            return render_template('activeuser.html', data= "invalid", project=wsProject, total=total, fileExists=False)
    return render_template('activeuser.html', data= data, project=wsProject, total=total, fileExists=True)

@app.route('/logs')
def logs():
    with open("jobs.log", "r") as f:
        logList = f.readlines()
    if logList == []:
        return render_template('logs.html', logExists = False, logs = [])
    else:
        return render_template('logs.html',logExists = True, logs = logList)

if __name__ == '__main__':
    app.run()

