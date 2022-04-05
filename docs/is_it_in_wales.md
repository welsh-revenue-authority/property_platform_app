# Is it in Wales?

[Try it out](https://land-property-platform.herokuapp.com/docs#/default/is_it_in_wales_is_it_in_wales_post)

Determine if a property is in wales.

## Endpoints

`https://land-property-platform.herokuapp.com/is_it_in_wales`


## Parameters

__uprn:__ (integer) The UPRN of the property (don't know it? search 
[here](https://www.findmyaddress.co.uk/search))


## Examples

### Requests
Request body:
```console
{
    "uprn": 10015308931
}
```

Or curl request:
```console
curl -X 'POST' \
  'https://land-property-platform.herokuapp.com/is_it_in_wales' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "uprn": 10015308931
}'
```

Or using python:
```python
import requests
import json


uprn = 10015308931
json_data = json.dumps({"uprn": uprn})
response = requests.post(
    "https://land-property-platform.herokuapp.com/is_it_in_wales",
    data=json_data,
)
```

### Response

Response body example:
```console
{
    "in_wales": "true"
}
```
Response body schema:
```console
{
    "in_wales": string
}
```

Possible "in_wales" values:

* "true" -- The property is in Wales
* "false" -- The property is not in Wales
* "partially" -- The property has been manually flagges as partially in Wales
and partially in England
