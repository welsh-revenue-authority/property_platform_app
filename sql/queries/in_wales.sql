-- cross-boarder example uprn 10093284081
-- not cross-boarder example uprn 10024827644 
-- england example uprn 10014514734
SELECT
    -- Want to extract true, false and partially (when property is flagged as
    -- cross_boarder which is an attribute)
    -- Note: There isn't error handling for non-exitent uprn
    CASE
        -- Check if cross_boarder attribute exists
        WHEN EXISTS (
            SELECT attribute_type
            FROM register.attributes
            INNER JOIN register.points USING(platform_property_id)
            WHERE uprn = 10014514734
            AND attribute_type = 'cross_boarder'
        ) THEN 'partially'
        
        WHEN (
            -- Full is it in wales geospacial query
            SELECT ST_Contains(wales, uprn)
            FROM 
                -- Wales polygon beside uprn point
                (SELECT
                    (SELECT geom FROM register.polygons WHERE platform_polygon_id = 2) AS wales,
                    (SELECT geom FROM register.points WHERE uprn = 10014514734) AS uprn
                ) as in_wales_check
            ) THEN 'true'
        ELSE 'false' 
    END AS in_wales
FROM register.points
WHERE uprn = 10014514734;
