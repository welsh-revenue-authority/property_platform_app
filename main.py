from typing import Union, List
from datetime import datetime
import re
import os

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
import fastapi_metadata as docs
import land_registry.transaction_data

# from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ltt.calculator import calculate_tax, tax_zone_lookup, tax_zone_lookup_polygon
from ltt.data_object_models import PropertyInfo, PropertyInfoRequest, Uprn, Address
from ltt.property_info import get_property_info
from ltt.location_checks import in_wales
from ltt.ltt_rate import land_transaction_tax_rate_query, land_transaction_tax_category_query, land_transaction_tax_threshold_query
from ltt.use_class import use_class_part_query, use_class_query
from ltt.council_tax import council_tax_band_query, council_tax_rate_query


api_keys = [
    os.environ.get("API_KEY")
]  # This will be encrypted in the database

oauth2_scheme = HTTPBearer() #OAuth2PasswordBearer(tokenUrl="/token")  # use token authentication

def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    api_key=api_key.dict()['credentials']
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

# App instantiation and setup
app = FastAPI(
    title="Land and property platform",
    description=docs.DESCRIPTION,
    openapi_tags=docs.TAGS_METADATA,
    contact=docs.CONTACT,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# security = HTTPBasic()
regex_alphanumeric = re.compile(r'[A-Za-z0-9, ]+')
regex_date = re.compile(r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])')

# Routes
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/getting-started", response_class=HTMLResponse, include_in_schema=False)
def pricing(request: Request):
    return templates.TemplateResponse("getting-started.html", {"request": request})


@app.get("/data", response_class=HTMLResponse, include_in_schema=False)
def data(request: Request):
    return templates.TemplateResponse("data.html", {"request": request})


@app.get("/analysts", response_class=HTMLResponse, include_in_schema=False)
def analysts(request: Request):
    return templates.TemplateResponse("analysts.html", {"request": request})


@app.get("/features", response_class=HTMLResponse, include_in_schema=False)
def features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})


@app.get("/roadmap", response_class=HTMLResponse, include_in_schema=False)
def roadmap(request: Request):
    return templates.TemplateResponse("roadmap.html", {"request": request})


@app.get("/poc-data", response_class=HTMLResponse, include_in_schema=False)
def poc_data(request: Request):
    return templates.TemplateResponse("poc-data.html", {"request": request})


@app.get("/features", response_class=HTMLResponse, include_in_schema=False)
def features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})


@app.get("/analysts", response_class=HTMLResponse, include_in_schema=False)
def analysts(request: Request):
    return templates.TemplateResponse("analysts.html", {"request": request})


@app.get("/api-docs", response_class=HTMLResponse, include_in_schema=False)
def apidocs(request: Request):
    return templates.TemplateResponse("apidocs.html", {"request": request})


@app.get("/getting-started", response_class=HTMLResponse, include_in_schema=False)
def pricing(request: Request):
    return templates.TemplateResponse("getting-started.html", {"request": request})


@app.get("/robots.txt", response_class=PlainTextResponse, include_in_schema=False)
def robots(request: Request):
    with open("static/robots.txt") as f:
        text = f.read()
    return text


# Test get API
# @app.get("/api")
# def read_api_root():
#     return {"Hello": "World"}


# Test post api
@app.post("/LLTT_calculator", tags=["LLTT_calculator"])
def lltt_calculator(property_info: Union[PropertyInfo, List[PropertyInfo]]):
    """
    Returns localised LTT tax for each set of property infos
    """

    # If only a single set of info is supplied turn into list so all can be
    # handled the same.
    if isinstance(property_info, PropertyInfo):
        property_info = [property_info]

    taxes = []
    for prop in property_info:
        tax = calculate_tax(
            address=prop.address,
            value=prop.value,
            attributes=prop.attributes,
            use_polygon=prop.use_polygon,
        )
        taxes.append(tax)

    return taxes


@app.post("/property_info", tags=["property_info"])
def property_info(property_info_request: PropertyInfoRequest):
    """
    Given an identifier, property information is returned. Some user groups may
    get access to all property data and some a restricted set.

    User groups: Welsh public sector, public
    """
    if not (
        property_info_request.platform_property_id or property_info_request.address
    ):
        return {"error": "one from platform_property_id or address must be provided"}

    return get_property_info(
        platform_property_id=property_info_request.platform_property_id,
        address=property_info_request.address,
        privacy_level=1,
    )


@app.post("/property_info_sensitive", tags=["property_info_sensitive"])
def property_info_sensitive(property_info_request: PropertyInfoRequest):
    """
    Given an identifier, property information is returned. Some user groups may
    get access to all property data and some a restricted set.

    User groups: Welsh public sector
    """
    if not (
        property_info_request.platform_property_id or property_info_request.address
    ):
        return {"error": "one from platform_property_id or address must be provided"}

    return get_property_info(
        platform_property_id=property_info_request.platform_property_id,
        address=property_info_request.address,
        privacy_level=2,
    )


@app.post("/is_it_in_wales", tags=["is_it_in_wales"])
def is_it_in_wales(uprn: Uprn):
    """
    Returns if a UPRN is in wales.
    """
    return {"in_wales": in_wales(uprn.uprn)}


@app.post("/tax_zones", tags=["tax_zones"])
def tax_zones(address: Address):
    """
    Returns a set of tax zones in which the property resides and to what
    proportion.

    Default uses point location lookup or set use_polygon to true to search
    by land extent.
    """
    if address.use_polygon:
        lookup_func = tax_zone_lookup_polygon
    else:
        lookup_func = tax_zone_lookup

    return lookup_func(address.address)

@app.post("/land_transaction_tax_rate", tags=["land_transaction_tax_rate"])
def land_transaction_tax_rate(geography_id: Union[str, None] = None):
    """
    Returns land transaction tax rate.
    """
    if not geography_id:
        return {"land_transaction_tax_rate": land_transaction_tax_rate_query()}
    if not re.fullmatch(regex_alphanumeric, geography_id):
        raise HTTPException(status_code=400, detail="Alphanumeric input expected")
    return {"land_transaction_tax_rate": land_transaction_tax_rate_query(geography_id)}

@app.post("/land_transaction_tax_category", tags=["land_transaction_tax_category"])
def land_transaction_tax_category():
    """
    Returns land transaction tax category.
    """
    return {"land_transaction_tax_category": land_transaction_tax_category_query()}

@app.post("/land_transaction_tax_threshold", tags=["land_transaction_tax_threshold"])
def land_transaction_tax_threshold():
    """
    Returns current land transaction tax thresholds.
    """
    return {"land_transaction_tax_threshold": land_transaction_tax_threshold_query()}

@app.post("/use_class", tags=["use_class"])
def use_class():
    """
    Returns use class.
    """
    return {"use_class": use_class_query()}

@app.post("/use_class_part", tags=["use_class_part"])
def use_class_part():
    """
    Returns use class part.
    """
    return {"use_class_part": use_class_part_query()}

@app.post("/council_tax_band", tags=["council_tax_band"])
def council_tax_band():
    """
    Returns current council tax bands.
    """
    return {"council_tax_band": council_tax_band_query()}

@app.post("/council_tax_rate", tags=["council_tax_rate"])
def council_tax_rate(geography_id: Union[str, None] = None):
    """
    Returns current council tax rates.
    """
    if not geography_id:
        return {"council_tax_rate": council_tax_rate_query()}
    if not re.fullmatch(regex_alphanumeric, geography_id):
        raise HTTPException(status_code=400, detail="Alphanumeric input expected")
    return {"council_tax_rate": council_tax_rate_query(geography_id)}

@app.get("/test_api_key", dependencies=[Depends(api_key_auth)], tags=["Auth"])
def test_api_key() -> dict:
    """
    Test your API Key.
    """
    return {
        "data": "You used a valid API key."
    }

@app.get("/load_transaction_data", dependencies=[Depends(api_key_auth)], tags=["Auth"])
def load_transaction_data(postcode_list, start_date="2018-04-01") -> dict:
    """
    Load LR transaction data into the platform.
    """
    if not postcode_list or not re.fullmatch(regex_alphanumeric, postcode_list):
        raise HTTPException(status_code=400, detail="Postcode: alphanumeric input expected")
    if not start_date or not re.fullmatch(regex_date, start_date):
        raise HTTPException(status_code=400, detail="start_date: yyyy-mm-dd date expected")
    transaction_started_timestamp = datetime.now()
    count = land_registry.transaction_data.get_transaction_data(postcode_list, start_date)
    land_registry.transaction_data.update_collection_log("lr_transactions",start_date,None,postcode_list,count,transaction_started_timestamp)
    return {
        "transaction_started_timestamp": transaction_started_timestamp,
        "postcode": postcode_list,
        "data": count
    }

@app.post("/lr_transaction_stats", tags=["lr_transactions"])
def lr_transaction_stats(postcode_area: Union[str, None] = None, start_date: str = "2018-04-01", end_date: Union[str, None] = None):
    """
    LR transactions stats \n
    start_date: starting date in yyyy-mm-dd format (optional) \n
    end_date: ending date in yyyy-mm-dd format \n
    postcode_area (optional): filter by comma separated postcode areas (don't use spaces). Leave postcode_area empty to get stats for all postcodes.
    """
    if postcode_area:
        if not re.fullmatch(regex_alphanumeric, postcode_area):
            raise HTTPException(status_code=400, detail="Alphanumeric input expected")
        postcode_area=postcode_area.replace(",","','")
    if not start_date or not re.fullmatch(regex_date, start_date):
        raise HTTPException(status_code=400, detail="start_date: yyyy-mm-dd date expected")
    if end_date and not re.fullmatch(regex_date, end_date):
        raise HTTPException(status_code=400, detail="end_date: yyyy-mm-dd date expected")

    return {"lr_transaction_stats": land_registry.transaction_data.stats_by_postcode_query(postcode_area, start_date, end_date)}

@app.post("/lr_transaction_stats_custom_area", tags=["lr_transactions"])
def lr_transaction_stats_custom_area(geometry_string: str, start_date: str = "2018-04-01", end_date: Union[str, None] = None):
    """
    LR transactions stats \n
    start_date: starting date in yyyy-mm-dd format (optional) \n
    end_date: ending date in yyyy-mm-dd format \n
    geometry_string: custom area in geoJSON format - polygon coordinates
    """
    # { "type": "Polygon", "coordinates": [ [ [ -3.644105790164972, 51.784366908033675 ], [ -3.20124639660477, 51.788184661426442 ], [ -3.189793136426489, 51.284241213582071 ], [ -3.590657242666327, 51.28805896697483 ], [ -3.644105790164972, 51.784366908033675 ] ] ] } 
    if not start_date or not re.fullmatch(regex_date, start_date):
        raise HTTPException(status_code=400, detail="start_date: yyyy-mm-dd date expected")
    if end_date and not re.fullmatch(regex_date, end_date):
        raise HTTPException(status_code=400, detail="end_date: yyyy-mm-dd date expected")

    return {"lr_transaction_stats": land_registry.transaction_data.stats_by_custom_area_query(geometry_string, start_date, end_date)}

@app.post("/lr_transaction_postcode_coverage", tags=["lr_transactions"])
def lr_transaction_postcode_coverage(postcode_valid_from_date: Union[int, None] = None, postcode_valid_to_date: Union[int, None] = None):
    """
    Returns LR transactions postcode coverage. \n
    postcode_valid_from_date: integer in yyyymm format (optional) \n
    postcode_valid_to_date: integer in yyyymm format (optional) 
    """
    #if postcode_valid_from_date and not re.fullmatch(regex_date, postcode_valid_from_date):
    #    raise HTTPException(status_code=400, detail="end_date: yyyy-mm-dd date expected")
    return {"lr_transaction_postcode_coverage": land_registry.transaction_data.postcode_coverage(postcode_valid_from_date, postcode_valid_to_date)}  

# @app.post("/sold_price")
# def sold_price():
#     """
#     Returns information on last sold price. May return multiple results as WRA
#     get this info instantly on transaction but land registry have a lag of
#     several weeks (return both?).
#
#     User groups: estate agenst, public
#     """
#     return {"status": "API not yet available"}
#
#
# @app.post("/property_tax_band")
# def property_tax_band():
#     """
#     Given an identifier, the properties tax band is returned. Restricted
#     access.
#
#     User groups: local authorities
#     """
#     return {"status": "API not yet available"}
#
#
# @app.post("/tax_zone")
# def tax_zone():
#     """
#     Given a property identifier, the tax zone in which the property resides is
#     returned.
#
#     User groups: all
#     """
#     return {"status": "API not yet available"}
