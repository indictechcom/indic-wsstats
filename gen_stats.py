# -*- coding: utf-8 -*-
import toolforge
import json
import datetime

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

siteData= {
        "as": {
                "namespace": {
                        "page": 104,
                        "index": 106
                },
                "category": {
                        "Without_text": "পাঠ্য_নথকা",
                        "Not_proofread": "মুদ্ৰণ_সংশোধন_কৰা_হোৱা_নাই",
                        "Problematic": "সমস্যাজৰ্জৰ",
                        "Proofread": "মুদ্ৰণ_সংশোধন",
                        "Validated": "বৈধকৰণ"
                }
        },
        "bn": {
                "namespace": {
                        "page": 104,
                        "index": 102
                },
                "category": {
                        "Without_text": "লেখাবিহীন",
                        "Not_proofread": "মুদ্রণ_সংশোধন_করা_হয়নি",
                        "Problematic": "সমস্যাসঙ্কুল",
                        "Proofread": "মুদ্রণ_সংশোধন_করা_হয়েছে",
                        "Validated": "বৈধকরণ"
                }
        },
        "gu": {
                "namespace": {
                        "page": 104,
                        "index": 106
                },
                "category": {
                        "Without_text": "લખાણ_રહિત",
                        "Not_proofread": "ભૂલશુદ્ધિ_બાકી",
                        "Problematic": "સમસ્યારૂપ",
                        "Proofread": "ભૂલશુદ્ધિ",
                        "Validated": "પ્રમાણિત"
                }
        },
        "kn": {
                "namespace": {
                        "page": 104,
                        "index": 106
                },
                "category": {
                        "Without_text": "ಪಠ್ಯವಿಲ್ಲದ್ದು",
                        "Not_proofread": "ಪರಿಶೀಲಿಸಲಾಗಿಲ್ಲ",
                        "Problematic": "ಸಮಸ್ಯಾಪೂರ್ಣ",
                        "Proofread": "ಪರಿಶೀಲಿಸಿದವು",
                        "Validated": "ಪ್ರಕಟಿಸಿದವು"
                }
        },
        "ml": {
                "namespace": {
                        "page": 106,
                        "index": 104
                },
                "category": {
                        "Without_text": "എഴുത്ത്_ഇല്ലാത്തവ",
                        "Not_proofread": "തെറ്റുതിരുത്തൽ_വായന_നടന്നിട്ടില്ലാത്തവ",
                        "Problematic": "പ്രശ്നമുള്ളവ",
                        "Proofread": "തെറ്റുതിരുത്തൽ_വായന_കഴിഞ്ഞവ",
                        "Validated": "സാധൂകരിച്ചവ"
                }
        },
        "mr": {
                "namespace": {
                        "page": 104,
                        "index": 106
                },
                "category": {
                        "Without_text": "मजकुराविना",
                        "Not_proofread": "तपासणी_करायचे_साहित्य",
                        "Problematic": "समस्यादायक",
                        "Proofread": "मुद्रितशोधन",
                        "Validated": "प्रमाणित"
                }
        },
        "or": {
                "namespace": {
                        "page": 250,
                        "index": 252
                },
                "category": {
                        "Without_text": "ଲେଖାନଥିବା",
                        "Not_proofread": "ପ୍ରମାଣିତ_ହୋଇନଥିବା",
                        "Problematic": "ଅସୁବିଧାଥିବା",
                        "Proofread": "ସଂଶୋଧନ",
                        "Validated": "ବୈଧ_କରାଗଲା"
                }
        },
        "pa": {
                "namespace": {
                        "page": 250,
                        "index": 252
                },
                "category": {
                        "Without_text": "ਲਿਖਤ_ਤੋਂ_ਬਿਨਾਂ",
                        "Not_proofread": "ਗਲਤੀਆਂ_ਨਹੀਂ_ਲਾਈਆਂ",
                        "Problematic": "ਸਮੱਸਿਆਤਮਕ",
                        "Proofread": "ਗਲਤੀਆਂ_ਲਾਈਆਂ",
                        "Validated": "ਪ੍ਰਮਾਣਿਤ"
                }
        },
        "sa": {
                "namespace": {
                        "page": 104,
                        "index": 106
                },
                "category": {
                        "Without_text": "लेखरहितम्",
                        "Not_proofread": "अपरिष्कृतम्",
                        "Problematic": "समस्यात्मकः",
                        "Proofread": "परिष्कृतम्",
                        "Validated": "पुष्टितम्"
                }
        },
        "ta": {
                "namespace": {
                        "page": 250,
                        "index": 252
                },
                "category": {
                        "Without_text": "உரை_இல்லாமல்",
                        "Not_proofread": "மெய்ப்பு_பார்க்கப்படாதவை",
                        "Problematic": "சிக்கலானவை",
                        "Proofread": "மெய்ப்புப்_பார்க்கப்பட்டவை",
                        "Validated": "சரிபார்க்கப்பட்டவை"
                }
        },
        "te": {
                "namespace": {
                        "page": 104,
                        "index": 106
                },
                "category": {
                        "Without_text": "పాఠ్యం_లేనివి",
                        "Not_proofread": "అచ్చుదిద్దబడని",
                        "Problematic": "సమస్యాత్మకం",
                        "Proofread": "అచ్చుదిద్దబడినవి",
                        "Validated": "ఆమోదించబడ్డవి"
                }

        }
}


def doCatQueery(category, namespace):
    return "select count(cl_from) as number from categorylinks where cl_to='%s' and cl_from in (select page_id from page where page_namespace=%s)"% ( category, namespace)


def updateJson(domain, num_allpages, num_q0, num_q1, num_q2, num_q3q4, num_q4, num_main_allpages, main_withscan, main_withoutscan):

        jsonFile = open("Stats.json", "r")  # Open the JSON file for reading
        data = json.load(jsonFile)  # Read the JSON into the buffer
        jsonFile.close()  # Close the JSON file

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

        ## Save our changes to JSON file
        jsonFile = open("Stats.json", "w+")
        jsonFile.write(json.dumps(data, indent= True))
        jsonFile.close()

for domain in domains:
        dbname = domain + 'wikisource_p'

        conn = toolforge.connect( dbname )
        cur = conn.cursor()

        pageNsCode = siteData[domain]['namespace']['page']

        # Get all page in Page namespace
        num_allpages = "select count(page_id) as number from page where page_namespace=%s and page_is_redirect=0"% (pageNsCode)
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
        main_withscan = "select count(distinct tl_from) as num from templatelinks left join page on page_id=tl_from where tl_namespace=%d and page_namespace=0;"%pageNsCode
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

        updateJson( domain, num_allpages, num_q0, num_q1, num_q2, num_q3+num_q4, num_q4, num_main_allpages, main_withscan, main_withoutscan )

        cur.close ()
        conn.close ()

# timestamp
jsonFile = open("Stats.json", "r")  # Open the JSON file for reading
data = json.load(jsonFile)  # Read the JSON into the buffer
jsonFile.close()  # Close the JSON file

data["timestamp"] = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

jsonFile = open("Stats.json", "w+")
jsonFile.write(json.dumps(data, indent= True))
jsonFile.close()