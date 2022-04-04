"""
For location checking fucntions
"""

from ltt.db_connections import sql_query


def in_wales(uprn: int):
    """Returns if a UPRN is in Wales"""
    result = sql_query(
        f"""
        SELECT
            -- Want to extract true, false and partially (when property is flagged as
            -- cross_boarder which is an attribute)
            -- Note: There isn't error handling for non-exitent uprn
            CASE
                -- Check if cross_boarder attribute exists
                WHEN EXISTS (
                    SELECT attribute_type
                    FROM register.attributes
                    INNER JOIN register.points USING(wra_property_id)
                    WHERE uprn = {uprn}
                    AND attribute_type = 'cross_boarder'
                ) THEN 'partially'
                
                WHEN (
                    -- Full is it in wales geospacial query
                    SELECT ST_Contains(wales, uprn)
                    FROM 
                        -- Wales polygon beside uprn point
                        (SELECT
                            -- Wales polygon has id 2 (more stable that filetering by descroption)
                            (SELECT geom FROM register.polygons WHERE wra_polygon_id = 2) AS wales,
                            (SELECT geom FROM register.points WHERE uprn = {uprn}) AS uprn
                        ) as in_wales_check
                    ) THEN 'true'
                ELSE 'false' 
            END AS in_wales
        FROM register.points
        JOIN register.properties USING(wra_property_id)
        WHERE uprn = {uprn};
    """
    )
    result = result[0][0]
    return result
