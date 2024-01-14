SELECT b.behaviour, t.date, t.time, t.latitude_mid, t.longitude_mid, season
FROM transect_log t, behaviour b, observations, name
WHERE t.gis_key = observations.gis_key
AND observations.species_code = name.code
AND name.code = :image_name
AND observations.behaviour_code = b.code
ORDER BY date, time;