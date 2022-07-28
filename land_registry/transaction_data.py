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

            SELECT ?transaction_id ?property_address ?paon ?saon ?street ?town ?county ?postcode ?amount ?transaction_date ?category ?property_type ?record_status ?estate_type ?new_build
            WHERE
            {
            {?property_address
                    text:query ( lrcommon:postcode "(""" + postcode_list + """)" 3000000 ) .

            ?property_address lrcommon:postcode ?postcode.

            ?transx lrppi:propertyAddress ?property_address ;
                    lrppi:transactionId     ?transaction_id;
                    lrppi:pricePaid ?amount ;
                    lrppi:transactionDate ?transaction_date ;
                    lrppi:transactionCategory/skos:prefLabel ?category.
            FILTER ( ?transaction_date >= "2018-04-01"^^xsd:date )
            }
            OPTIONAL {?property_address lrcommon:county ?county}
            OPTIONAL {?property_address lrcommon:paon ?paon}
            OPTIONAL {?property_address lrcommon:saon ?saon}
            OPTIONAL {?property_address lrcommon:street ?street}
            OPTIONAL {?property_address lrcommon:town ?town}
            OPTIONAL { ?transx  lrppi:propertyType  ?property_type }
            OPTIONAL { ?transx  lrppi:recordStatus  ?record_status }
            OPTIONAL { ?transx  lrppi:estateType  ?estate_type }
            OPTIONAL { ?transx  lrppi:newBuild  ?new_build }
            }
            ORDER BY ?amount
        """
    }

    r = requests.post(url = api_url, headers=headers, data = data)
    jsonData = r.json()
    jsonData = json.loads(jsonData['result'])['results']['bindings']
    rows = []
    cols = ["transaction_id", "property_address", "paon" , "saon", "street" , "town" , "county" , "postcode" , "amount" , "transaction_date" , "category", "property_type", "record_status", "estate_type", "new_build"]
    for x in jsonData:
        row = []
        for col in cols:
            value = x.get(col)
            if not value:
                row.append(None)
                continue

            match col:
                case "amount":
                    row.append(int(value.get('value')))
                case "property_address":
                    row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/data/ppi/address/",""))
                case "property_address":
                    row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/data/ppi/address/",""))
                case "property_type":
                    row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/def/common/",""))
                case "record_status":
                    row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/def/ppi/",""))
                case "estate_type":
                    row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/def/common/",""))
                case _:
                    row.append(str(value.get('value')))

        row.append(x.get('postcode').get('value').split()[0])
        rows.append(row)
    #"INSERT into lr_transactions(paon , street, town , county , postcode, amount, transaction_date , category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    sql_bulk_insert("lr_transactions", "transaction_id, lr_property_address_id, paon , saon, street, town , county , postcode, amount, transaction_date , category, property_type, record_status, estate_type, new_build, postcode_area", rows)
    return len(jsonData)

def stats_by_postcode_query():
    """Returns LR transactions stats"""
    result = sql_query_json(
        f"""
        SELECT postcode_area, min(amount), max(amount), avg(amount), count(amount) FROM public.lr_transactions group by postcode_area;
        """
    )
    return result

