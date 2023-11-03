-- Rank bands, with 'Glam Rock' style, based on their longeity
-- Longevity is based on `split - formed`
SELECT band_name, 
       CASE
           WHEN split IS NULL THEN '2022'
           ELSE split
       END - formed AS lifespan
  FROM metal_bands
 WHERE IFNULL(style, '') LIKE '%Glam rock%'
 ORDER BY lifespan DESC;
