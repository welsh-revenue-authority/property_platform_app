import logging
import time
from datetime import datetime
from land_registry.transaction_data import get_transaction_data, update_collection_log
from ltt.postcode import load_postcode_boundaries_by_area

# Postcode areas entirely in Wales
POSTCODE_AREAS_ENTIRELY_IN_WALES = ["CF","LL","SA","SY"]
# Postcode areas partially in Wales
# ["CH","LD","HR","NP"]
# Postcode zones - Wales only (where the Area is partially in Wales)
#["LD1","LD2","LD3","LD4","LD5","LD6","LD7","LD8","CH1","CH4","CH5","CH6","CH7","CH8","GL16","HR3","HR5","NP1","NP10","NP11","NP12","NP13","NP15","NP16","NP18","NP19","NP2","NP20","NP22","NP23","NP24","NP25","NP26","NP3","NP4","NP44","NP5","NP6","NP7","NP8","NP9","NPT"]
ALL_POSTCODE_ZONES = ["CF1","CF10","CF11","CF14","CF15","CF2","CF23","CF24","CF3","CF30","CF31","CF32","CF33","CF34","CF35","CF36","CF37","CF38","CF39","CF4","CF40","CF41","CF42","CF43","CF44","CF45","CF46","CF47","CF48","CF5","CF6","CF61","CF62","CF63","CF64","CF7","CF71","CF72","CF8","CF81","CF82","CF83","CF91","CF95","CF99","CH1","CH4","CH5","CH6","CH7","CH8","GL16","HR3","HR5","LD1","LD2","LD3","LD4","LD5","LD6","LD7","LD8","LL11","LL12","LL13","LL14","LL15","LL16","LL17","LL18","LL19","LL20","LL21","LL22","LL23","LL24","LL25","LL26","LL27","LL28","LL29","LL30","LL31","LL32","LL33","LL34","LL35","LL36","LL37","LL38","LL39","LL40","LL41","LL42","LL43","LL44","LL45","LL46","LL47","LL48","LL49","LL51","LL52","LL53","LL54","LL55","LL56","LL57","LL58","LL59","LL60","LL61","LL62","LL63","LL64","LL65","LL66","LL67","LL68","LL69","LL70","LL71","LL72","LL73","LL74","LL75","LL76","LL77","LL78","LD1","LD2","LD3","LD4","LD5","LD6","LD7","LD8","CH1","CH4","CH5","CH6","CH7","CH8","GL16","HR3","HR5","NP1","NP10","NP11","NP12","NP13","NP15","NP16","NP18","NP19","NP2","NP20","NP22","NP23","NP24","NP25","NP26","NP3","NP4","NP44","NP5","NP6","NP7","NP8","NP9","NPT","SA1","SA10","SA11","SA12","SA13","SA14","SA15","SA16","SA17","SA18","SA19","SA2","SA20","SA3","SA31","SA32","SA33","SA34","SA35","SA36","SA37","SA38","SA39","SA4","SA40","SA41","SA42","SA43","SA44","SA45","SA46","SA47","SA48","SA5","SA6","SA61","SA62","SA63","SA64","SA65","SA66","SA67","SA68","SA69","SA7","SA70","SA71","SA72","SA73","SA8","SA80","SA9","SA99","SY10","SY13","SY14","SY15","SY16","SY17","SY18","SY19","SY20","SY21","SY22","SY23","SY24","SY25","SY5","SY7","SY9"]

def transaction_data():
    postcode_areas_to_load = []
    start_date = "2018-04-01"
    for postcode_area in postcode_areas_to_load:
        print(postcode_area)
        transaction_started_timestamp = datetime.now()
        count = get_transaction_data(postcode_area, start_date)
        print(count)
        update_collection_log("lr_transactions",start_date,None,postcode_area,count,transaction_started_timestamp)
        time.sleep(0.5)

def postcodes():
    postcode_areas_to_load = []
    for postcode_area in postcode_areas_to_load:
        # Wildcart (*) may be used, when requesting whole postcode area (CF*)
        load_postcode_boundaries_by_area("C:\\Users\\user\\Downloads\\1\\gb-postcodes-v5\\units\\"+postcode_area+".geojson", postcode_area)
    print("[ DONE ]")

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    postcodes()
    print("[ DONE ]")