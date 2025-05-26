CREATE or REPLACE VIEW Poluentes_por_Bairro AS
SELECT
	pla.name AS bairro,
    pol.name AS poluente,
    AVG(pol.value) AS media_valor
FROM
	gold.pollutants_data AS pol
RIGHT JOIN gold.places AS pla
	ON pla.id = pol.place_id
GROUP BY 
	pla.name, pol.name
ORDER BY pol.name, pla.name

CREATE OR REPLACE VIEW gold.media_temperatura_por_bairro_e_dia AS
	SELECT
	    p.name as bairro,
	    DATE_TRUNC('day', wd.created_at) AS data,
	    ROUND(AVG(wd.temperature), 2) AS temperatura_media
	FROM
	    gold.weather_data AS wd
	JOIN
		gold.places AS p ON p.id = wd.place_id
	GROUP BY
	    bairro, data
	ORDER BY
	    bairro ASC, data ASC

CREATE OR REPLACE VIEW gold.media_humidade_por_bairro_e_dia AS
	SELECT
	    p.name as bairro,
	    DATE_TRUNC('day', wd.created_at) AS data,
	    ROUND(AVG(wd.humidity), 2) AS humidade_media
	FROM
	    gold.weather_data AS wd
	JOIN
		gold.places AS p ON p.id = wd.place_id
	GROUP BY
	    bairro, data
	ORDER BY
	    bairro ASC, data ASC

-- Teste a view
SELECT * FROM gold.poluentes_por_bairro
