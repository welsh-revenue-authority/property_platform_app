"""
Data models for api post request structures.

Note: to nest models / suport nested json apis, make another, model for each 
level
"""

import datetime
from typing import Union, Optional, Any
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


class PropertyInfoRequest(BaseModel):
    wra_property_id: Optional[int] = None
    address: Optional[str] = None


# Database entity models
class Attribute(BaseModel):
    wra_property_id: int
    attribute_type: str
    bool_value: Optional[bool] = None
    text_value: Optional[str] = None
    numeric_value: Optional[Union[int, float]] = None
    valid_from: Optional[str] = str(datetime.date.today())
    valid_to: Optional[str] = None
    wra_attribute_id: Optional[int] = None

    @property
    def value(self) -> Any:
        if self.bool_value:
            return self.bool_value
        elif self.text_value:
            return self.text_value
        elif self.numeric_value:
            return self.numeric_value
        else:
            return
