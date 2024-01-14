SELECT year, species, behaviour FROM bdaylist
WHERE mmdd = :udate
GROUP BY year, species, behaviour
ORDER BY year ASC;