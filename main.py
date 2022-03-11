from typing import Union, Optional, Dict, List
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
#from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ltt.calculator import calculate_tax


# Post request data models
class PropertyInfo(BaseModel):
    address: str
    value: Union[float, int]
    attributes: Optional[Dict[str, Union[int, float, bool, str]]] = {}
    use_polygon: Optional[bool] = None


# App instantiation and setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
#security = HTTPBasic()

# Routes
# Landing page
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Test get API
@app.get("/api")
def read_api_root():
    return {"Hello": "World"}


# Test post api
@app.post("/LTT_tax")
def test_api(property_info: Union[PropertyInfo, List[PropertyInfo]]):
    """Returns LTT tax for each set of property infos"""
    # If only a single set of info is supplied turn into list so all can be 
    # handled the same.
    if isinstance(property_info, PropertyInfo):
        property_info = [property_info]

    taxes = []
    for prop in property_info:
        tax = calculate_tax(**prop.dict())
        taxes.append(tax)

    return taxes

