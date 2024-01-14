SELECT CONCAT(n.species,' (', n.type,')') AS species, SUM(o.count) AS sightings
FROM observations AS o, name AS n
WHERE o.species_code = n.code
GROUP BY n.species, n.type
ORDER BY sightings DESC;

