import requests
import json

from typing import Union
from ltt.db_connections import sql_insert, sql_insert_bulk, sql_query_json

def get_transaction_data(postcode_list, start_date):
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
            FILTER ( ?transaction_date >= \""""+start_date+"""\"^^xsd:date )
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

            if col=="amount":
                row.append(int(value.get('value')))
            elif col=="property_address":
                row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/data/ppi/address/",""))
            elif col=="property_address":
                row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/data/ppi/address/",""))
            elif col=="property_type":
                row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/def/common/",""))
            elif col=="record_status":
                row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/def/ppi/",""))
            elif col=="estate_type":
                row.append(str(value.get('value')).replace("http://landregistry.data.gov.uk/def/common/",""))
            else:
                row.append(str(value.get('value')))

        # postcode_area
        row.append(x.get('postcode').get('value').split()[0])
        # postcode_clean
        row.append(x.get('postcode').get('value').strip().replace(' ',''))

        rows.append(row)

    #"INSERT into lr_transactions(paon , street, town , county , postcode, amount, transaction_date , category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    sql_insert_bulk("lr_transactions", "transaction_id, lr_property_address_id, paon , saon, street, town , county , postcode, amount, transaction_date , category, property_type, record_status, estate_type, new_build, postcode_area, postcode_clean", rows)
    return len(jsonData)

def update_collection_log(data_set, start_date, end_date, query_filter_value, results_count, transaction_date):
    sql_insert("collection_log", "data_set, start_date, end_date, query_filter_value, results_count, transaction_date", [data_set, start_date, end_date, query_filter_value, results_count, transaction_date], "%s, %s, %s, %s, %s, %s")

def stats_by_postcode_query(postcode_area: Union[str, None] = None, start_date: Union[str, None] = None, end_date: Union[str, None] = None):
    """Returns LR transactions stats"""
    query="""SELECT postcode_area, min(amount), max(amount), avg(amount), count(amount) FROM public.lr_transactions """
    if(postcode_area or start_date or end_date):
        query+= "WHERE "
    if(postcode_area):
        query+= f"""postcode_area IN ('"""+postcode_area+"""')"""
        if(start_date or end_date):
           query+= " AND " 
    if start_date:
        query+= "transaction_date>='"+start_date+"'"
        if end_date:
            query+= " AND "
    if end_date:
        query+= "transaction_date<='"+end_date+"'"
    query += f""" GROUP BY postcode_area ORDER BY postcode_area;"""
    result = sql_query_json(query)
    return result

def stats_by_custom_area_query(geometry_string: str, start_date: Union[str, None] = None, end_date: Union[str, None] = None):
    """LR transactions stats for the custom area"""
    query="""SELECT min(amount), max(amount), avg(amount), count(amount) FROM public.lr_transactions INNER JOIN wales_postcode_points_ons_may2022 ON postcode_clean=pcd2_clean """
    query+= "WHERE "
    query+= f"""ST_Intersects( ST_SetSRID(geom,4326), ST_SetSRID(ST_GeomFromGeoJSON(%(geometry_string)s),4326) )"""
    if(start_date or end_date):
        query+= " AND " 
    if start_date:
        query+= "transaction_date>='"+start_date+"'"
        if end_date:
            query+= " AND "
    if end_date:
        query+= "transaction_date<='"+end_date+"'"
    result = sql_query_json(query, {"geometry_string": geometry_string})
    return result

def postcode_coverage(postcode_valid_from_date: Union[int, None] = None, postcode_valid_to_date: Union[int, None] = None):
    """Returns LR transactions postcode coverage."""
    q=f"""SELECT postcode_area FROM public.lr_transactions """
    if(postcode_valid_from_date or postcode_valid_to_date):
        q+=f"""INNER JOIN wales_postcode_points_ons_may2022 ON postcode_clean=pcd2_clean WHERE """
    if(postcode_valid_from_date):
        q+=f"""(doterm is null OR doterm >="""+str(postcode_valid_from_date)+""")"""
        if(postcode_valid_to_date):
            q+=f"""AND """
    if(postcode_valid_to_date):
            q+=f"""dointr<="""+str(postcode_valid_to_date)+""" AND doterm<="""+str(postcode_valid_to_date)
    q+=""" group by postcode_area ORDER BY postcode_area;"""
    result = sql_query_json(q)
    return result