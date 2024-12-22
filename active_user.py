from config import domains, siteData
import toolforge
import json
import sys
from typing import Dict, List, Optional, TypedDict

class UserStats(TypedDict):
    proofread: str
    validate: str

class DomainStats(TypedDict):
    users: Dict[str, UserStats]

class PageStatus(TypedDict):
    proofread: Optional[Dict[str, str]]
    validate: Optional[Dict[str, str]]

from pywikisource import WikiSourceApi

statsUser: Dict[str, Dict[str, UserStats]] = {}
time: str = sys.argv[1]

for domain in domains:
    # Define variables
    statsUser[domain] = {}
    usr: Dict[str, List[str]] = {}
    activity: Dict[str, UserStats] = {}

    dbname: str = domain + 'wikisource_p'
    WS: WikiSourceApi = WikiSourceApi(domain)
    conn = toolforge.connect(dbname)
    cur = conn.cursor()

    pageNsCode: int = siteData[domain]['namespace']['page']

    # SQL Query to get active user with page edit in Page namespace
    q: str = "select rev_id, actor_id, actor_name, page_id, page_title " \
    "from revision inner join actor on actor.actor_id = rev_actor " \
    "inner join page on page.page_id = rev_page " \
    "where rev_timestamp > '"+ time + "01000000' and rev_timestamp < '" + time + "31235959' " \
    "and page_namespace = "+ str(pageNsCode) + " and actor_user != '' order by actor_name;"

    # Execute SQL Query
    cur.execute(q)
    rows = cur.fetchall()

    # Create usr dict with list of page edits
    for row in rows:
        user: str = str(row[2].decode("utf-8"))

        if user in usr:
            usr[user].append(str(row[4].decode("utf-8")))
        else:
            usr[user] = []
            usr[user].append(str(row[4].decode("utf-8")))

    # Process the pages edit by users
    for k, v in usr.items():
        prcount: int = 0
        valcount: int = 0

        # Used set for unique list
        for page in list(set(v)):
            pstatus: PageStatus = WS.pageStatus('Page:'+ page)

            # To count proofread
            if (pstatus["proofread"] is not None 
                and pstatus["proofread"].get("user") == k 
                and pstatus["proofread"].get("timestamp")[0:7].replace('-', '') == time
            ):
                prcount = prcount + 1

            # To count validation
            if (pstatus["validate"] is not None 
                and pstatus["validate"].get("user") == k 
                and pstatus["validate"].get("timestamp")[0:7].replace('-', '') == time
            ):
                valcount = valcount + 1

        # Store the count
        activity[k] = {
            "proofread": str(prcount),
            "validate": str(valcount)
        }

        statsUser[domain] = activity

with open("ActiveUserStats/" + time + ".json", "w") as f:
    json.dump(statsUser, f, ensure_ascii=False, sort_keys=True, indent=True)
