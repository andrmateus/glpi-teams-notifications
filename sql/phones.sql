SELECT
            gp.id,
            gp.name AS hostname,
            gs.completename AS status,
            gm.name AS fabricante,
            gl.completename AS localizacao,
            gpm.name AS modelo,
            gpfp.ndalinhacomdddfield AS linha,
            gu.name AS usuario,
            gp.serial AS numero_de_serie,
            gpt.name AS tipo,
            gpfp.imeizeroonefield AS imei
        FROM
            glpi_phones gp
            INNER JOIN glpi_plugin_fields_phonetelefones gpfp ON gpfp.items_id = gp.id
            INNER JOIN glpi_users gu ON gu.id = gp.users_id
            INNER JOIN glpi_phonetypes gpt ON gpt.id = gp.phonetypes_id
            INNER JOIN glpi_states gs ON gs.id = gp.states_id
            INNER JOIN glpi_manufacturers gm ON gm.id = gp.manufacturers_id
            INNER JOIN glpi_locations gl ON gl.id = gp.locations_id
            INNER JOIN glpi_phonemodels gpm ON gpm.id = gp.phonemodels_id
        WHERE
            gp.is_deleted = 0