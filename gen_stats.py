# -*- coding: utf-8 -*-
import toolforge
# import json
import datetime
from typing import Dict, TypedDict, Optional
from config import domains, siteData
from app import app
from models import db, LanguageStats


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

def doCatQueery(category: str, namespace: int) -> str:
    return "select count(cl_from) as number from categorylinks where cl_to='%s' and cl_from in (select page_id from page where page_namespace=%s)" % (
    category, namespace)

def updateDatabase(domain, num_allpages, num_q0, num_q1, num_q2, num_q3q4, num_q4, num_main_allpages, main_withscan,
               main_withoutscan, main_apg, page_aps, timestamp):

        with app.app_context():  # Open the JSON file for reading
                try:
                language_stat = LanguageStats(
                        language_code=domain,
                        main_aps=main_apg,
                        main_pages=num_main_allpages,
                        main_with_out_scan=main_withoutscan,
                        main_with_scan=main_withscan,
                        not_proofread=num_q1,
                        num_of_pages=num_allpages,
                        page_aps=page_aps,
                        problematic=num_q2,
                        proofread=num_q3q4,
                        validated=num_q4,
                        without_text=num_q0,
                        timestamp = timestamp
                )
                db.session.add(language_stat)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error updating database for domain {domain}: {e}")

#get the timestamp
timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")


for domain in domains:
        dbname: str = domain + 'wikisource_p'

        conn = toolforge.connect(dbname)
        cur = conn.cursor()

        pageNsCode: int = siteData[domain]['namespace']['page']

        # Get all page in Page namespace
        num_allpages_query: str = "select count(page_id) as number from page where page_namespace=%s and page_is_redirect=0" % pageNsCode
        cur.execute(num_allpages_query)
        row = cur.fetchone()
        num_allpages: int = int(row[0])

        # Get Q0
        cur.execute(doCatQueery(siteData[domain]['category']['Without_text'], pageNsCode))
        row = cur.fetchone()
        num_q0: int = int(row[0])

        # Get Q1
        cur.execute(doCatQueery(siteData[domain]['category']['Not_proofread'], pageNsCode))
        row = cur.fetchone()
        num_q1: int = int(row[0])

        # Get Q2
        cur.execute(doCatQueery(siteData[domain]['category']['Problematic'], pageNsCode))
        row = cur.fetchone()
        num_q2: int = int(row[0])

        # Get Q3
        cur.execute(doCatQueery(siteData[domain]['category']['Proofread'], pageNsCode))
        row = cur.fetchone()
        num_q3: int = int(row[0])

        # Get Q4
        cur.execute(doCatQueery(siteData[domain]['category']['Validated'], pageNsCode))
        row = cur.fetchone()
        num_q4: int = int(row[0])

        # Get main namespace's total pages
        num_main_allpages_query: str = "select count(distinct page_id) from page where page_namespace=0 and page_is_redirect=0;"
        cur.execute(num_main_allpages_query)
        row = cur.fetchone()
        num_main_allpages: int = int(row[0])

        # Get main namespace's with scan
        main_withscan_query: str = "select count(distinct tl_from) as num from templatelinks left join page on page_id=tl_from where tl_from_namespace=%d and page_namespace=0;" % pageNsCode
        cur.execute(main_withscan_query)
        row = cur.fetchone()
        main_withscan: int = int(row[0])

        #Get Disambiguation pages
        q_disamb: str = "select count(page_title) from page where page_namespace = 0 and page_is_redirect = 0 and page_id in (select pp_page from page_props where pp_propname = 'disambiguation')"
        cur.execute(q_disamb)
        row = cur.fetchone()
        num_disambig: int = int(row[0])

        # Get main namespace's without scan
        main_withoutscan: int = num_main_allpages - main_withscan - num_disambig

        # Get Average Page Size
        main_apg_query: str = "select avg(page_len) from page where page_namespace = 0;"
        cur.execute(main_apg_query)
        row = cur.fetchone()
        main_apg: int = int(row[0])

        page_aps_query: str = "select avg(page_len) from page where page_namespace = %d;" % pageNsCode
        cur.execute(page_aps_query)
        row = cur.fetchone()
        page_aps: int = int(row[0])

        updateDatabase(domain, num_allpages, num_q0, num_q1, num_q2, num_q3 + num_q4, num_q4, num_main_allpages,
                   main_withscan, main_withoutscan, main_apg, page_aps, timestamp)

        cur.close()
        conn.close()

