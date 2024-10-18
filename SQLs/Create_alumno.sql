CREATE TABLE `alumno` (
	`IdAlumno` INT(11) NOT NULL AUTO_INCREMENT,
	`IdAula` INT(11) NOT NULL,
	`NombreAlum` VARCHAR(500) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`Ciclo` VARCHAR(200) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`Curso` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`Grupo` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`CreatedAt` TIMESTAMP NULL DEFAULT current_timestamp(),
	`UpdatedAt` DATETIME NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	PRIMARY KEY (`IdAlumno`) USING BTREE,
	INDEX `fk_IdAula` (`IdAula`) USING BTREE,
	CONSTRAINT `fk_IdAula` FOREIGN KEY (`IdAula`) REFERENCES `aula` (`IdAula`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=61
;
