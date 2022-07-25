"""
For use class checking functions
"""

from ltt.db_connections import sql_query_json


def use_class_query():
    """Returns current use classes"""
    result = sql_query_json(
        f"""
        SELECT *
	    FROM public.use_class WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    )
    return result
    
def use_class_part_query():
    """Returns current use class part"""
    result = sql_query_json(
        f"""
        SELECT *
	    FROM public.use_class_part WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    )
    return result