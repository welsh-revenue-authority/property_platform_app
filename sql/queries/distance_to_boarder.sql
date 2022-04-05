-- Returns table with each uprn from Upper Leadworth and distance to welsh 
-- boarder
-- Note: platform_plygon_id for wales shape is 2 (more robust to use this than
-- description as it's unique)
SELECT 
    uprn
  , platform_property_id
  , ST_Distance(
      geom, 
      (
        SELECT ST_Boundary(geom)
		FROM register.polygons
		WHERE platform_polygon_id = 2
	  )
    ) AS distance_to_boarder
FROM register.points
JOIN register.properties USING(platform_property_id)
WHERE address LIKE '%Upper Leadworth'
ORDER BY distance_to_boarder
LIMIT 10;
