"""
Module for FastAPI meta data for sqagger docs.

NB: This is not part of Mkdocs and should not be referenced in mkdocs.yml
"""

DESCRIPTION = """
__PROOF OF CONCEPT - CONTAINS FAKE DATA - APIS NOT STABLE OR TESTED__

A collection of APIs to serve data from a centralised property register for
Wales.

Use these APIs to request information about properties in Wales.
"""
TAGS_METADATA = [
        {
            "name": "property_info",
            "description": "get all information on a property"
        },
        {
            "name": "LTT_tax",
            "description": "calculate localised land transaction tax"
        },
        {
            "name": "is_it_in_wales",
            "description": "find out if a property (UPRN) is in Wales"
        }
        ]
CONTACT = {
        "name": "Property Data Platform PoC project",
        "url": "https://welsh-revenue-authority.github.io/property-data-poc/en/",
        "email": "dataproject@wra.gov.wales"
    }
