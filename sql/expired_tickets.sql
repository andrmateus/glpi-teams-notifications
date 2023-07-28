SELECT
	gt.id `id`
    ,gg.name `fila_atendimento`
FROM
	glpi_tickets gt
	INNER JOIN glpi_groups_tickets ggt ON ggt.tickets_id = gt.id
    left JOIN (select *, case
                    when name like "Field BA%" then "NORDESTE"
                    when name like "Field MG UMC%" then "HOSPITAIS"
                    when name like "Field PB%" then "NORDESTE"
                    when name like "Field PE%" then "NORDESTE"
                    when name like "Field SE%" then "NORDESTE"
                    when name like "Field DF%" then "CENTRO-OESTE"
                    when name like "Field GO%" then "CENTRO-OESTE"
                    when name like "Field PR%" then "SUL"
                    when name like "Field SC%" then "SUL"
                    when name like "Field RS%" then "SUL"
                    when name like "Field RJ%" then "RIO"
                    when name like "Field ES%" then "RIO"
                    when name like "Field SP%" then "SP"
                    when name like "Field MG%" then "MG"
                    when name like "Suporte CSO%" then "MG"
                    when name like "Gestão de Ativos%" then "CENTRAL"
                    when name like "Suporte Simpress%" then "CENTRAL"
                    when name like "Central%" then "CENTRAL"
            end `region` from glpi_groups) gg ON gg.id = ggt.groups_id
WHERE
	gt.is_deleted = 0 and
	gt.`status` IN (1,2,3) and
	ggt.`type` = 2 AND
	gg.groups_id in(198, 295) AND
    gt.time_to_resolve < now();