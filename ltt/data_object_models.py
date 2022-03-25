"""
Data models for api post request structures.

Note: to nest models / suport nested json apis, make another, model for each 
level
"""

import datetime
from typing import Union, Optional
from pydantic import BaseModel


# External data (json structure) models
class Attributes(BaseModel):
    second_home: Optional[bool]
    buy_to_let: Optional[bool]
    attribute_a: Optional[int]
    attribute_b: Optional[int]


class PropertyInfo(BaseModel):
    address: str
    value: Union[float, int]
    attributes: Optional[Attributes] = None
    use_polygon: Optional[bool] = None


# Database entity models
class Attribute(BaseModel):
    wra_property_id: int
    attribute_type: str
    bool_value: Optional[bool] = None
    text_value: Optional[str] = None
    numeric_value: Optional[Union[int, float]] = None
    valid_from: Optional[str] = str(datetime.date.today())
    valid_to: Optional[str] = None
