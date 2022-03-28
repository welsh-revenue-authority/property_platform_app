# Property Information API
Use this api to get all available information on a property.

## Example
Request body:

```console
{
    "address": "58, Mountain Road, Pontypandy"
}
```

Response body:
```console
{
    "wra_property_id": 6,
    "address": "58, Mountain Road, Pontypandy",
    "attributes": {
        "attribute_a": 2,
        "buy_to_let": true,
        "attribute_b": 3
    }
}
```

## How to Use
This is a REST API. Send a post request to url: 
[https://land-property-platform.herokuapp.com/property_info](https://land-property-platform.herokuapp.com/property_info)
with a JSON body with either an __address__ field or a __wra_property_id__ field.

A respose with all available information on the property will be returned. *Note
that this is for illustrative purposes and will return fake data. Future API 
calls that return real data mak require security clearance.*

Response shcema:

```console
{
    # Property identifiers (request will have identified one of these)
    "wra_property_id": integer,
    "address": string,
    # Property attributes
    "attributes": {
        "attribute": attribite value,
        ... : ...
    }
}
```
## Attributes
Attributes contain the know information on the property.

### second_home
__Attribute name:__ "second_home"<br>
__Possible values:__ true, false<br>
__Description:__ If true, the property is not a main residence.<br>

### buy_to_let
__Attribute name:__ "buy_to_let"<br>
__Possible values:__ true, false<br>
__Description:__ If true, the property is considered a buy-to-let property. 
Note that a property is not identified as a second home if it is a buy-to-let
property.<br>

### attribute_a
__Attribute name:__ "attribute_a"<br>
__Possible values:__ 1, 2<br>
__Description:__ A placeholder attribute which can hold integer values and has
a multiplier effect on LLT.<br>

### attribute_b
__Attribute name:__ "attribute_b"<br>
__Possible values:__ 1, 2, 3<br>
__Description:__ A placeholder attribute which can hold integer values and has
a fixed addition effect on LLT.<br>
