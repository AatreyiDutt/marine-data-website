SELECT CONCAT(n.species,' (', n.type,')') AS species, COUNT(o.behaviour_code) AS occurences
FROM name AS n, observations AS o
WHERE o.behaviour_code=:bcode AND o.species_code=n.code
GROUP BY n.species, n.type
ORDER BY occurences DESC;