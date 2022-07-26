import requests
import json

from typing import Union
from ltt.db_connections import sql_bulk_insert, sql_query_json

def get_transaction_data(postcode_list):
    api_url = "https://landregistry.data.gov.uk/app/root/qonsole/query"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://landregistry.data.gov.uk",
        "Referer": "https://landregistry.data.gov.uk/app/qonsole",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62"
    }

    data = {
        'output':'json',
        'url':'/landregistry/query',
        'q': """
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            prefix sr: <http://data.ordnancesurvey.co.uk/ontology/spatialrelations/>
            prefix ukhpi: <http://landregistry.data.gov.uk/def/ukhpi/>
            prefix lrppi: <http://landregistry.data.gov.uk/def/ppi/>
            prefix skos: <http://www.w3.org/2004/02/skos/core#>
            prefix lrcommon: <http://landregistry.data.gov.uk/def/common/>
            PREFIX  text: <http://jena.apache.org/text#>

            # Returns the Price Paid data from the default graph for each transaction record having
            # an address with the given postcode.
            # The postcode to query is set using SPARQL 1.1's 'values' clause

            SELECT ?paon ?street ?town ?county ?postcode ?amount ?date ?category
            WHERE
            {
            {?addr
                    text:query ( lrcommon:postcode "(""" + postcode_list + """)" 3000000 ) .

            ?addr lrcommon:postcode ?postcode.

            ?transx lrppi:propertyAddress ?addr ;
                    lrppi:pricePaid ?amount ;
                    lrppi:transactionDate ?date ;
                    lrppi:transactionCategory/skos:prefLabel ?category.
            FILTER ( ?date >= "2018-04-01"^^xsd:date )
            }
            OPTIONAL {?addr lrcommon:county ?county}
            OPTIONAL {?addr lrcommon:paon ?paon}
            OPTIONAL {?addr lrcommon:saon ?saon}
            OPTIONAL {?addr lrcommon:street ?street}
            OPTIONAL {?addr lrcommon:town ?town}
            }
            ORDER BY ?amount
        """
    }

    r = requests.post(url = api_url, headers=headers, data = data)
    jsonData = r.json()
    jsonData = json.loads(jsonData['result'])['results']['bindings']
    rows = []
    cols = ["paon" , "street" , "town" , "county" , "postcode" , "amount" , "date" , "category"]
    for x in jsonData:
        row = []
        for col in cols:
            value = x.get(col)
            if not value:
                row.append(None)
            elif(col=="amount"):
                row.append(int(value.get('value')))
            else:
                row.append(str(value.get('value')))
        row.append(x.get('postcode').get('value').split()[0])
        rows.append(row)
    #"INSERT into lr_transactions(paon , street, town , county , postcode, amount, transaction_date , category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    sql_bulk_insert("lr_transactions", "paon , street, town , county , postcode, amount, transaction_date , category, postcode_area", rows)
    return len(jsonData)

def stats_by_postcode_query():
    """Returns LR transactions stats"""
    result = sql_query_json(
        f"""
        SELECT postcode_area, min(amount), max(amount), avg(amount), count(amount) FROM public.lr_transactions group by postcode_area;
        """
    )
    return result

