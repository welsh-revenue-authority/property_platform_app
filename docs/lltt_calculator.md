# Localised Land Transaction Tax Calculator?

[Try it out](https://land-property-platform.herokuapp.com/docs#/default/LLTT_calculator/test_api_LLTT_calculator_post)

Calculate the localised land transaction tax for a property in Wales.

## Endpoints

`https://land-property-platform.herokuapp.com/LLTT_calculator`


## Parameters

__address:__ (string) The address of the property<br>
__value:__ (integer) The sale value of the property in GBP<br>
__attributes:__ (json) Key : Value attributes of the property. Options: 
```console
__second_home__: (true | false)
__buy_to_let__: (true | false)
__attribute_a:__ (1 | 2)
__attribute_b:__ (1 | 2 | 3)
```
__use_polygon:__ (boolean) If true the plygon land extent asociated with the 
property will be used to determine the tax zone. Extents crossing zone boarders
will be apportioned appropriately.

## Examples

### Requests
Simple request body:
```console
{
  "address": "199, Mountain Road, Upper Leadworth",
  "value": 200000
}
```

Or curl request:
```console
curl -X 'POST' \
  'https://land-property-platform.herokuapp.com/LLTT_calculator' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "address": "199, Mountain Road, Upper Leadworth",
  "value": 200000
}'
```

Or using python:
```python
import requests
import json


address = "199, Mountain Road, Upper Leadworth"
value = 200000
json_data = json.dumps({"address": address, "value": value})
response = requests.post(
    "https://land-property-platform.herokuapp.com/LLTT_calculator",
    data=json_data,
)
```

Request body containing attributes:
```console
{
  "address": "199, Mountain Road, Upper Leadworth",
  "value": 200000,
  "attributes": {
    "second_home": true
  }
}
```

Request body containing attributes and use_polygon:
```console
{
  "address": "1, Pontypandy",
  "value": 150000,
  "attributes": {
    "buy_to_let": true,
    "attribute_a": 2
  },
  "use_polygon": true
}
```

Multiple jsons can be sent in a json array and will recieve a list of results 
in the response

### Response

Response body example:
```console
[
    8650
]
```

Or for json array requests:
```console
[
    8650,
    9650.5
]
```

Response body schema:
```console
[
    integer | float
]
```

