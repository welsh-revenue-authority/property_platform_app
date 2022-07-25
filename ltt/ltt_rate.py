"""
For ltt rate checking functions
"""

from ltt.db_connections import sql_query_json


def land_transaction_tax_rate_query(geography_id: str):
    """Returns current land transaction tax rates for given geography"""
    result = sql_query_json(
        f"""
        SELECT * 
        FROM public."land_transaction_tax_rate" WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL) AND "geography_id"='{geography_id}';
        """
    )
    return result

def land_transaction_tax_category_query():
    """Returns current land transaction tax categories"""
    result = sql_query_json(
        f"""
        SELECT *
        FROM public."land_transaction_tax_category"
        WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    )
    return result

def land_transaction_tax_threshold_query():
    """Returns current land transaction tax thresholds"""
    result = sql_query_json(
        f"""
        SELECT *
        FROM public.land_transaction_tax_threshold 
        WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    )
    return result
