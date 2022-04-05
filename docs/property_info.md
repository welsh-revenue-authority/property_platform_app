# Property Information API

[Try it out](https://land-property-platform.herokuapp.com/docs#default/property_info_property_info_post)

Find all information on a given property.


## Endpoints

`https://land-property-platform.herokuapp.com/property_info`


## Parameters

__platform_property_id:__ (integer) The platform_property_id

__address:__ (string) The address of the property as found in the database,

## Examples
Request body:

```console
{
    "address": "58, Mountain Road, Pontypandy"
}
```

Response body:
```console
{
    "platform_property_id": 6,
    "address": "58, Mountain Road, Pontypandy",
    "attributes": {
        "attribute_a": 2,
        "buy_to_let": true,
        "attribute_b": 3
    }
}
```

Response schema:

```console
{
    # Property identifiers (request will have identified one of these)
    "platform_property_id": integer,
    "address": string,
    # Property attributes
    "attributes": {
        "attribute": attribite value,
        ... : ...
    }
}
```


### Attributes
Attributes contain the know information on the property.

#### Second home
__Attribute name:__ "second_home"<br>
__Possible values:__ true, false<br>
__Description:__ If true, the property is not a main residence.<br>

#### Buy_to_let
__Attribute name:__ "buy_to_let"<br>
__Possible values:__ true, false<br>
__Description:__ If true, the property is considered a buy-to-let property. 
Note that a property is not identified as a second home if it is a buy-to-let
property.<br>

#### Attribute a
__Attribute name:__ "attribute_a"<br>
__Possible values:__ 1, 2<br>
__Description:__ A placeholder attribute which can hold integer values and has
a multiplier effect on LLT.<br>

#### Attribute b
__Attribute name:__ "attribute_b"<br>
__Possible values:__ 1, 2, 3<br>
__Description:__ A placeholder attribute which can hold integer values and has
a fixed addition effect on LLT.<br>
