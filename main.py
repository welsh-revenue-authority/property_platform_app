from typing import Union, List
import re

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

# from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ltt.calculator import calculate_tax, tax_zone_lookup, tax_zone_lookup_polygon
from ltt.data_object_models import PropertyInfo, PropertyInfoRequest, Uprn, Address
from ltt.property_info import get_property_info
from ltt.location_checks import in_wales
from ltt.ltt_rate import land_transaction_tax_rate_query, land_transaction_tax_category_query
from ltt.use_class import use_class_part_query, use_class_query
import fastapi_metadata as docs


# App instantiation and setup
app = FastAPI(
    title="Land and property platform",
    description=docs.DESCRIPTION,
    openapi_tags=docs.TAGS_METADATA,
    contact=docs.CONTACT,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# security = HTTPBasic()
alphaNumeric = re.compile(r'[A-Za-z0-9]+')

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
def land_transaction_tax_rate(geography_id: str):
    """
    Returns land transaction tax rate.
    """
    if not re.fullmatch(alphaNumeric, geography_id):
        raise HTTPException(status_code=400, detail="Alphanumeric input expected")
    return {"land_transaction_tax_rate": land_transaction_tax_rate_query(geography_id)}

@app.post("/land_transaction_tax_rate", tags=["land_transaction_tax_rate"])
def land_transaction_tax_category():
    """
    Returns land transaction tax rate.
    """
    return {"land_transaction_tax_category": land_transaction_tax_category_query()}

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
