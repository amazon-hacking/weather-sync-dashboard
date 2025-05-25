create or replace view Poluentes_por_Bairro as
select
	pla.name as bairro,
    pol.name as poluente,
    AVG(pol.value) as media_valor
from 
	gold.pollutants_data as pol
right join gold.places as pla
	on pla.id = pol.place_id
group by 
	pla.name, pol.name
order by pol.name, pla.name

CREATE VIEW gold.media_temperatura_por_bairro_e_dia AS
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

CREATE VIEW gold.media_humidade_por_bairro_e_dia AS
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

CREATE VIEW gold.media_temperatura_por_bairro_e_mes AS
	SELECT
	    p.name AS bairro,
	    DATE_TRUNC('month', wd.created_at) AS data,
	    ROUND(AVG(wd.temperature), 2) AS temperatura_media
	FROM
	    gold.weather_data AS wd
	JOIN
		gold.places AS p ON p.id = wd.place_id
	GROUP BY
	    bairro, data
	ORDER BY
	    bairro ASC, data ASC

CREATE VIEW gold.media_humidade_por_bairro_e_mes AS
	SELECT
	    p.name AS bairro,
	    DATE_TRUNC('month', wd.created_at) AS data,
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
select * from gold.poluentes_por_bairro
