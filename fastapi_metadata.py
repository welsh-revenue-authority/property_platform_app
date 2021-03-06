"""
Module for FastAPI meta data for sqagger docs.

NB: This is not part of Mkdocs and should not be referenced in mkdocs.yml
"""

DESCRIPTION = """

This is a proof of concept created by the Welsh Revenue Authority. It contains 
synthetic data and does not cover the whole of Wales. [Find out more about what 
data is included in the proof of concept](https://land-property-platform.herokuapp.com/poc-data).

"""
TAGS_METADATA = [
    {
        "name": "property_info",
        "description": "get all public information on a property",
    },
    {
        "name": "property_info_sensitive",
        "description": "get all information on a property",
    },
    {
        "name": "LLTT_calculator",
        "description": "calculate localised land transaction tax",
    },
    {
        "name": "is_it_in_wales",
        "description": "find out if a property (UPRN) is in Wales",
    },
    {
        "name": "tax_zones",
        "description": "find out which LLTT tax zone(s) a property is within",
    },
]
CONTACT = {
    "name": "Property Data Platform PoC project",
    "url": "https://welsh-revenue-authority.github.io/property-data-poc/en/",
    "email": "dataproject@wra.gov.wales",
}
