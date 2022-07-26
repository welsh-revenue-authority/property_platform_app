"""
For council tax checking functions
"""

from typing import Union
from ltt.db_connections import sql_query_json


def council_tax_band_query():
    """Returns current council tax bands"""
    result = sql_query_json(
        f"""
        SELECT *
	    FROM public.council_tax_band WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    )
    return result
    
def council_tax_rate_query(geography_id: Union[str, None] = None):
    """Returns current council tax rates"""
    if(geography_id):
        q=f"""
        SELECT *
	    FROM public.council_tax_rate WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL) AND "geography_id"='{geography_id}';
        """
    else:
        q = f"""
        SELECT *
	    FROM public.council_tax_rate WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    result = sql_query_json(q)
    return result