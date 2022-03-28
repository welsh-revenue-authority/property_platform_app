from typing import Union, Optional, Dict, List
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ltt.calculator import calculate_tax
from ltt.data_object_models import PropertyInfo, PropertyInfoRequest
from ltt.property_info import get_property_info


# App instantiation and setup
app = FastAPI(title="Land and property tax platform")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# security = HTTPBasic()

# Routes
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get(
    "/about-the-platform", response_class=HTMLResponse, include_in_schema=False
)
def index(request: Request):
    return templates.TemplateResponse("datasets.html", {"request": request})


@app.get("/roadmap", response_class=HTMLResponse, include_in_schema=False)
def roadmap(request: Request):
    return templates.TemplateResponse("roadmap.html", {"request": request})


@app.get("/features", response_class=HTMLResponse, include_in_schema=False)
def features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})


@app.get("/analysts", response_class=HTMLResponse, include_in_schema=False)
def analysts(request: Request):
    return templates.TemplateResponse("analysts.html", {"request": request})


@app.get("/api-docs", response_class=HTMLResponse, include_in_schema=False)
def apidocs(request: Request):
    return templates.TemplateResponse("apidocs.html", {"request": request})


@app.get("/pricing", response_class=HTMLResponse, include_in_schema=False)
def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})


# Test get API
@app.get("/api")
def read_api_root():
    return {"Hello": "World"}


# Test post api
@app.post("/LTT_tax")
def test_api(property_info: Union[PropertyInfo, List[PropertyInfo]]):
    """
    Returns LTT tax for each set of property infos
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


@app.post("/sold_price")
def sold_price():
    """
    Returns information on last sold price. May return multiple results as WRA
    get this info instantly on transaction but land registry have a lag of
    several weeks (return both?).

    User groups: estate agenst, public
    """
    return {"status": "API not yet available"}


@app.post("/property_info")
def property_info(property_info_request: PropertyInfoRequest):
    """
    Given an identifier, property information is returned. Some user groups may
    get access to all property data and some a restricted set.

    User groups: local authorities (full access), public (restricted access)
    """
    if (
        not property_info_request.wra_property_id
        or not property_info_request.address
    ):
        return {
            "error": "one from wra_property_id or address must be provided"
        }

    return get_property_info(
        wra_property_id=property_info_request.wra_property_id,
        address=property_info_request.address,
    )


@app.post("/property_tax_band")
def property_tax_band():
    """
    Given an identifier, the properties tax band is returned. Restricted
    access.

    User groups: local authorities
    """
    return {"status": "API not yet available"}


@app.post("/tax_zone")
def tax_zone():
    """
    Given a property identifier, the tax zone in which the property resides is
    returned.

    User groups: all
    """
    return {"status": "API not yet available"}
