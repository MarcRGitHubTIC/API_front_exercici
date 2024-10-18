CREATE TABLE `aula` (
	`IdAula` INT(11) NOT NULL AUTO_INCREMENT,
	`DescAula` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`Edificio` VARCHAR(200) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`Pis` INT(11) NULL DEFAULT NULL,
	`CreatedAt` TIMESTAMP NULL DEFAULT current_timestamp(),
	`UpdatedAt` DATETIME NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	PRIMARY KEY (`IdAula`) USING BTREE,
	UNIQUE INDEX `DescAula` (`DescAula`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=46
;
