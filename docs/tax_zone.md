# Tax Zone Lookup API

[Try it out](https://land-property-platform.herokuapp.com/docs#/tax_zones/tax_zones_tax_zones_post)

Find out which LLTT tax zone(s) a property resides in.


## Endpoints

`https://land-property-platform.herokuapp.com/tax_zone`


## Parameters

__address:__ (string) The address of the property as found in the database

__use_polygon:__ (string, optional) If true then the search will use the 
polygon associated with the address to search. This may reside in multiple tax
zones. Note: for this PoC only 3 addresses have associated polygons. Use 
examples below.


## Examples

### Requests

Request body:
```console
{
    "address": "58, Mountain Road, Pontypandy"
}
```

Or curl request:
```console
curl -X 'POST' \
  'https://land-property-platform.herokuapp.com/tax_zone' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "address": "58, Mountain Road, Pontypandy"
}'
```

Or using python:
```python
import requests
import json


address = "58, Mountain Road, Pontypandy"
json_data = json.dumps({"address": address})
response = requests.post(
    "https://land-property-platform.herokuapp.com/tax_zone",
    data=json_data,
)
```

Or if search by land extent is required:

```console
{
    "address": "1, Pontypandy",
    "use_polygon": true
}
```


### Response

Response body:
```console
{
  "north_zone": 1
}
```

Or with use_polygon set to true:
```console
{
  "north_zone": 0.8522164045055316,
  "south_zone": 0.14778359549447
}
```

Response schema:

```console
{
    tax_zone: proportion of property within
}
```

