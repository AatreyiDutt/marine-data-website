SELECT o.species_code, n.species
FROM observations o, name n
WHERE o.species_code=n.code 
GROUP BY o.species_code, n.species;