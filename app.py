#!/usr/bin/env python3

import json
from typing import Dict, List, Optional, TypedDict
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from config import domains, siteData
from models import db, LanguageStats
import datetime
import yaml, os

class StatsData(TypedDict):
    Num_of_pages: int
    Without_text: int
    Not_proofread: int
    Problematic: int
    Proofread: int
    Validated: int
    Main_Pages: int
    Main_WithScan: int
    Main_WithOutScan: int
    Main_APS: int
    Page_APS: int

class WikiStats(TypedDict):
    timestamp: str
    domains: Dict[str, StatsData]

class UserStats(TypedDict):
    proofread: str
    validate: str

__version__: str = "2.0"

app: Flask = Flask(__name__)
CORS(app)

# Load configuration from YAML file
dir = os.path.dirname(__file__)
app.config.update(yaml.safe_load(open(os.path.join(dir, 'config.yaml'))))
db.init_app(app)  # initialize db with flask app

@app.route('/')
def index() -> str:
    with app.app_context():
        all_stats = LanguageStats.query.all()
        data = {}
        for stat in all_stats:
            data[stat.language_code] = {
                "Num_of_pages": stat.num_of_pages,
                "Without_text": stat.without_text,
                "Not_proofread": stat.not_proofread,
                "Problematic": stat.problematic,
                "Proofread": stat.proofread,
                "Validated": stat.validated,
                "Main_Pages": stat.main_pages,
                "Main_WithScan": stat.main_with_scan,
                "Main_WithOutScan": stat.main_with_out_scan,
            }
        if all_stats:
             data['timestamp'] = all_stats[0].timestamp
        else:
            data['timestamp'] = "No data"
        print("data for index:",data)
      
    return render_template('index.html', domains=domains, data=data)

@app.route('/wikitable')
def wikitable() -> str:
    
    with app.app_context():
        all_stats = LanguageStats.query.all()
        data = {}
        for stat in all_stats:
            data[stat.language_code] = {
                "Num_of_pages":stat.num_of_pages,
                "Without_text":stat.without_text,
                "Not_proofread":stat.not_proofread,
                "Problematic":stat.problematic,
                "Proofread":stat.proofread,
                "Validated":stat.validated,
                "Main_Pages":stat.main_pages,
                "Main_WithScan":stat.main_with_scan,
                "Main_WithOutScan":stat.main_with_out_scan,
            }
        if all_stats:
             data['timestamp'] = all_stats[0].timestamp
        else:
            data['timestamp'] = "No data"


    wikiTable: str = "Statistics on " + data['timestamp']
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

    data.pop('timestamp', None)

    for domain in domains:

        wikiTable += f"""\n|-
|{domain} || {data[domain]['Num_of_pages']} || {data[domain]['Without_text']} || {data[domain]['Not_proofread']} || {data[domain]['Problematic']} || {data[domain]['Proofread']} || {data[domain]['Validated']} || {data[domain]['Main_Pages']} || {data[domain]['Main_WithScan']} || {data[domain]['Main_WithOutScan']} || {100 * data[domain]["Main_WithScan"] / (data[domain]["Main_WithScan"] + data[domain]["Main_WithOutScan"]):.2f}"""

    wikiTable += "\n|}"
    return render_template('wikitable.html', Wikitable=wikiTable)

# API
@app.route('/api/stats')
def statsAPI() -> WikiStats:
    with app.app_context():
        all_stats = LanguageStats.query.all()
        data = {}
        for stat in all_stats:
            data[stat.language_code] = {
                "Num_of_pages":stat.num_of_pages,
                "Without_text":stat.without_text,
                "Not_proofread":stat.not_proofread,
                "Problematic":stat.problematic,
                "Proofread":stat.proofread,
                "Validated":stat.validated,
                "Main_Pages":stat.main_pages,
                "Main_WithScan":stat.main_with_scan,
                "Main_WithOutScan":stat.main_with_out_scan,
                "timestamp":stat.timestamp
            }
    print("data for api:",data)

    return jsonify( data )

@app.route('/graph')
def graph() -> str:
    return render_template('graph.html')

@app.route('/activeuser')
def activeuser() -> str:
    wsProject: Optional[str] = request.args.get('project', None)
    wsMonth: Optional[str] = request.args.get('month', None)
    data: Optional[Dict[str, UserStats]] = None
    fileExists: bool = True
    total: Dict[str, int] = {
        "proofread": 0,
        "validate": 0
    }
    
    if wsMonth is not None:
        try:
            with open("ActiveUserStats/" + wsMonth + ".json", "r") as jsonFile:
                data = json.load(jsonFile)
            data = data[wsProject]

            # Count the total
            for count in data.values():
                total["proofread"] = total["proofread"] + int(count["proofread"])
                total["validate"] = total["validate"] + int(count["validate"])
            return render_template('activeuser.html', data=data, project=wsProject, total=total, fileExists=True)
        except FileNotFoundError:
            return render_template('activeuser.html', data="invalid", project=wsProject, total=total, fileExists=False)
    return render_template('activeuser.html', data=data, project=wsProject, total=total, fileExists=True)

@app.route('/logs')
def logs() -> str:
    with open("jobs.log", "r") as f:
        logList: List[str] = f.readlines()
    if not logList:
        return render_template('logs.html', logExists=False, logs=[])
    else:
        return render_template('logs.html', logExists=True, logs=logList)

if __name__ == '__main__':
    with app.app_context():
            db.create_all() 
    app.run()

