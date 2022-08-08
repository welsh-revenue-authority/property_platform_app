from db_connections import connect
import json
import logging
import sys
import io
import glob

INSERT_POSTCODE_AREA = 'INSERT INTO postcode_boundaries (geom, postcode, postcode_area, mapit_code) VALUES (ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326), %s, %s, %s);'

def import_feature(cur,feature_data):
    if feature_data.get('type') == 'FeatureCollection':
        for feature in feature_data['features']:
            import_feature(cur, feature)
    elif feature_data.get('type') == 'Feature':
        geojson = json.dumps(feature_data['geometry'])
        #str_dict = dict((unicode(k), unicode(v)) for k, v in feature_data['properties'].items())
        mapit_code = feature_data['properties'].get('mapit_code')
        postcode = feature_data['properties'].get('postcodes')
        postcode_area = postcode.split()[0]
        cur.execute(INSERT_POSTCODE_AREA, (geojson, postcode, postcode_area, mapit_code))

def load_postcode_boundaries_by_area(path_file_mask, postcode_area):
    handles = (glob.glob(path_file_mask))
    con = connect()
    print("Postcode area: " + postcode_area + "Number of files to process: "+str(len(handles)))
    for handle in handles:
        print(handle)
        handle = io.open(handle,'r')
        with handle:
            feature_data = json.load(handle)
        with con:
            with con.cursor() as cur:
                import_feature(cur, feature_data)
            con.commit()
    print("Area loaded: "+postcode_area)