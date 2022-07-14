"""
For use class checking functions
"""

from ltt.db_connections import sql_query


def use_class_query():
    """Returns use classes"""
    result = sql_query(
        f"""
        SELECT id, reference, use_class, use_class_part, name_en, name_cy, description_en, description_cy, usage_types_en, usage_types_cy, start_date, end_date
	    FROM public.use_class WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    )
    return result
    
def use_class_part_query():
    """Returns use class part"""
    result = sql_query(
        f"""
        SELECT id, reference, name_en, name_cy, description_en, description_cy, use_class_part, organisation, start_date, end_date
	    FROM public.use_class_part WHERE "start_date"<CURRENT_DATE AND ("end_date">CURRENT_DATE OR "end_date" is NULL);
        """
    )
    return result