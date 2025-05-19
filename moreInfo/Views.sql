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

-- Teste a view
select * from gold.poluentes_por_bairro