"""
Data models for api post request structures.

Note: to nest models / suport nested json apis, make another, model for each 
level
"""

from typing import Union, Optional
from pydantic import BaseModel


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
