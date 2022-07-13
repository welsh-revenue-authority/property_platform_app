"""
For location checking fucntions
"""

from ltt.db_connections import sql_query


def land_transaction_tax_rate_query(geography_id: str):
    """Returns land transaction tax rate"""
    result = sql_query(
        f"""
        SELECT id, description_en, description_cy, "lower-threshold", "upper-threshold", rate, "land-transaction-tax-category", "geography-id", organisation, "start-date", "end-date"
	FROM public."land-transaction-tax-rate" WHERE "start-date"<CURRENT_DATE AND ("end-date">CURRENT_DATE OR "end-date" is NULL) AND "geography-id"='{geography_id}';
    """
    )
    return result
