--CREATE virtual VIEW to use to find birthday sightings 
CREATE VIEW bdaylist AS
SELECT TO_CHAR(t.date, 'MM-DD') AS mmdd, TO_CHAR(t.date, 'YYYY') AS year, n.species, b.behaviour
FROM transect_log t, name n, behaviour b, observations o
WHERE n.code = o.species_code
AND o.behaviour_code = b.code
AND o.gis_key = t.gis_key;
