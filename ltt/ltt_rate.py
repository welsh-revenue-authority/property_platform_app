"""
For location checking fucntions
"""

from ltt.db_connections import sql_query


def land_transaction_tax_rate_query(geography_id: str):
    """Returns land transaction tax rate"""
    result = sql_query(
        f"""
        SELECT id, description_en, description_cy, "lower_threshold", "upper_threshold", rate, "land_transaction_tax_category", "geography_id", organisation, "start_date", "end_date"
	FROM public."land_transaction_tax_rate" WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL) AND "geography_id"='{geography_id}';
    """
    )
    return result
