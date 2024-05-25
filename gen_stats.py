# -*- coding: utf-8 -*-
import toolforge
import json
import datetime
from config import domains, siteData

def doCatQueery(category, namespace):
    return "select count(cl_from) as number from categorylinks where cl_to='%s' and cl_from in (select page_id from page where page_namespace=%s)" % (
    category, namespace)


def updateJson(domain, num_allpages, num_q0, num_q1, num_q2, num_q3q4, num_q4, num_main_allpages, main_withscan,
               main_withoutscan, main_apg, page_aps):

        with open("Stats.json", "r") as f:  # Open the JSON file for reading
                data = json.load(f)         # Read the JSON into the buffer

        ## Working with buffered content
        data[domain]["Num_of_pages"] = num_allpages
        data[domain]["Without_text"] = num_q0
        data[domain]["Not_proofread"] = num_q1
        data[domain]["Problematic"] = num_q2
        data[domain]["Proofread"] = num_q3q4
        data[domain]["Validated"] = num_q4
        data[domain]["Main_Pages"] = num_main_allpages
        data[domain]["Main_WithScan"] = main_withscan
        data[domain]["Main_WithOutScan"] = main_withoutscan
        data[domain]["Main_APS"] = main_apg
        data[domain]["Page_APS"] = page_aps

        # Save our changes to JSON file
        with open("Stats.json", "w+") as f:
                json.dump( data, f, indent= True)

for domain in domains:
        dbname = domain + 'wikisource_p'

        conn = toolforge.connect( dbname )
        cur = conn.cursor()

        pageNsCode = siteData[domain]['namespace']['page']

        # Get all page in Page namespace
        num_allpages = "select count(page_id) as number from page where page_namespace=%s and page_is_redirect=0" % pageNsCode
        cur.execute( num_allpages )
        row = cur.fetchone()
        num_allpages = int(row[0])

        # Get Q0
        cur.execute( doCatQueery( siteData[domain]['category']['Without_text'], pageNsCode) )
        row = cur.fetchone()
        num_q0 = int(row[0])

        # Get Q1
        cur.execute( doCatQueery( siteData[domain]['category']['Not_proofread'], pageNsCode) )
        row = cur.fetchone()
        num_q1 = int(row[0])

        # Get Q2
        cur.execute( doCatQueery( siteData[domain]['category']['Problematic'], pageNsCode) )
        row = cur.fetchone()
        num_q2 = int(row[0])

        # Get Q3
        cur.execute( doCatQueery( siteData[domain]['category']['Proofread'], pageNsCode) )
        row = cur.fetchone()
        num_q3 = int(row[0])

        # Get Q4
        cur.execute( doCatQueery( siteData[domain]['category']['Validated'], pageNsCode) )
        row = cur.fetchone()
        num_q4 = int(row[0])

        # Get main namespace's total pages
        num_main_allpages = "select count(distinct page_id) from page where page_namespace=0 and page_is_redirect=0;"
        cur.execute( num_main_allpages )
        row = cur.fetchone()
        num_main_allpages = int(row[0])

        # Get main namespace's with scan
        main_withscan = "select count(distinct tl_from) as num from templatelinks left join page on page_id=tl_from where tl_from_namespace=%d and page_namespace=0;"%pageNsCode
        cur.execute( main_withscan )
        row = cur.fetchone()
        main_withscan = int(row[0])

        #Get Disambiguation pages
        q_disamb = "select count(page_title) from page where page_namespace = 0 and page_is_redirect = 0 and page_id in (select pp_page from page_props where pp_propname = 'disambiguation')"
        cur.execute(q_disamb)
        row = cur.fetchone ()
        num_disambig = int(row[0])

        # Get main namespace's without scan
        main_withoutscan = num_main_allpages - main_withscan - num_disambig

        # Get Average Page Size
        main_apg = "select avg(page_len) from page where page_namespace = 0;"
        cur.execute(main_apg)
        row = cur.fetchone()
        main_apg = int(row[0])

        page_aps = "select avg(page_len) from page where page_namespace = %d;" % pageNsCode
        cur.execute(page_aps)
        row = cur.fetchone()
        page_aps = int(row[0])

        updateJson(domain, num_allpages, num_q0, num_q1, num_q2, num_q3 + num_q4, num_q4, num_main_allpages,
                   main_withscan, main_withoutscan, main_apg, page_aps)

        cur.close ()
        conn.close ()

# timestamp
with open("Stats.json", "r") as f: # Open the JSON file for reading
        data = json.load(f)        # Read the JSON into the buffer

data["timestamp"] = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

with open("Stats.json", "w") as f:
        json.dump( data, f, sort_keys=True, indent= True)
