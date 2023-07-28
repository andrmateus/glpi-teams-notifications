SELECT
	a.id
	,a.titulo
	,a.atribuido
	,gtv.submission_date `data_envio_aprovacao`
	,gu.name `aprovador`
FROM
	(SELECT
		gt.id
		,gic.completename `titulo`
		,gu.name `atribuido`
		,(SELECT a.id FROM glpi_ticketvalidations a where a.tickets_id = gt.id ORDER BY a.id DESC LIMIT 1) AS `validate`
	FROM 
		glpi_tickets gt
		INNER JOIN glpi_groups_tickets ggt ON ggt.tickets_id = gt.id
		INNER JOIN glpi_tickets_users gtu ON gtu.tickets_id = gt.id
		INNER JOIN glpi_users gu ON gu.id = gtu.users_id
	    inner join glpi_itilcategories gic on gic.id = gt.itilcategories_id
	WHERE 
		gt.is_deleted = 0
		AND ggt.`type` = 2
		AND ggt.groups_id = 271
		AND gt.`status` IN (1,2,3,4)
		AND gt.global_validation = 2
		AND gtu.`type` = 2
	ORDER BY validate ASC
	) AS `a`
	INNER JOIN glpi_ticketvalidations gtv ON gtv.id = a.validate
	INNER JOIN glpi_users gu ON gu.id = gtv.users_id_validate
WHERE date(gtv.submission_date) < DATE_SUB(NOW(),INTERVAL 8 day)