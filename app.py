#!/usr/bin/env python3

import json
import os
from flask import Flask, render_template, jsonify, request, \
    abort, redirect, url_for
from flask_jsonlocale import Locales
import requests
import urllib
from flask_cors import CORS
from config import domains
from flask_bootstrap import Bootstrap

__version__ = "2.0"

app = Flask(__name__)
app.config["MESSAGES_DIR"] = "messages"
app.config["SECRET_KEY"] = os.urandom(24)
locales = Locales(app)
_ = locales.get_message
CORS(app)
Bootstrap(app)

@app.route('/')
def index():
    jsonFile = open("Stats.json", "r")  # Open the JSON file for reading
    data = json.load(jsonFile)  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file
    data['timestamp'] = _('timestamp') # Ensure that the timestamp is updated in en.json
    return render_template('index.html', domains= domains, data= data)

@app.route('/wikitable')
def wikitable():

    jsonFile = open("Stats.json", "r")  # Open the JSON file for reading
    jsonData = json.load( jsonFile )  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file
    jsonData['timestamp'] = _('timestamp') # Ensure that the timestamp is updated in en.json
    wikiTable = _('stats') + " "+ jsonData[ 'timestamp']
    wikiTable += '{|' + f"""
class="wikitable sortable"
|-
! colspan="7" style="text-align:center;background: #ffffff;" | { _('page-ns') }
! colspan="4" style="text-align:center;background: #ffffff;" | { _('main-ns') }
|-
!style="background: #ffffff;"|'''{ _('lang') }'''
!style="background: #ffffff;"|'''{ _('all-pgs') }'''
!style="background: #ddd;"|'''{ _('no-text') }'''
!style="background: #ffa0a0;"|'''{ _('not-proofread') }'''
!style="background: #b0b0ff;"|'''{ _('problem') }'''
!style="background: #ffe867;"|'''{ _('proofread') }'''
!style="background: #90ff90;"|'''{ _('valid') }'''
!style="background: #ffffff;"|'''{ _('all-pgs') }'''
!style="background: #90ff90;"|'''{ _('scan') }'''
!style="background: #ffa0a0;"|'''{ _('no-scan') }'''
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
    jsonFile = open("Stats.json", "r")  # Open the JSON file for reading
    jsonData = json.load( jsonFile )  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file
    jsonData['timestamp'] = _('timestamp') # Ensure that the timestamp is updated in en.json
    return jsonify( jsonData )


@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/activeuser')
def activeuser():
    wsProject = request.args.get('project', None)
    wsMonth = request.args.get('month', None)
    data = None
    total = {
        "proofread": 0,
        "validate": 0
    }
    if wsMonth is not None:
        jsonFile = open("ActiveUserStats/" + wsMonth + ".json", "r")
        data = json.load( jsonFile )
        jsonFile.close()
        data = data[wsProject]

        # Count the total
        for count in data.values():
            total["proofread"] = total["proofread"] + int(count["proofread"])
            total["validate"] = total["validate"] + int(count["validate"])

    return render_template('activeuser.html', data= data, project=wsProject, total=total)

@app.route('/changelang', methods=['GET', 'POST'])
def changelang():
    if request.method == "POST":
        locales.set_locale(request.form['locale'])
        return redirect(url_for('index'))
    lcs = locales.get_locales()
    per_lce = locales.get_permanent_locale()
    return render_template('changelang.html', locales=lcs, permanent_locale=per_lce)

if __name__ == '__main__':
    app.run()
