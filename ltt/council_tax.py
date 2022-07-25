"""
For council tax checking functions
"""

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
    
def council_tax_rate_query():
    """Returns current council tax rates"""
    result = sql_query_json(
        f"""
        SELECT *
	    FROM public.council_tax_rate WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    )
    return result