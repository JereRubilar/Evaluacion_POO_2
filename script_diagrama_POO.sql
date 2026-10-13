-- Failsafe por si ya existe el schema --
DROP SCHEMA IF EXISTS `gestion_empleados`;

-- Creación de schema --
CREATE SCHEMA `gestion_empleados`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Creación de usuario para conectar con programa (importante cambiar las credenciales) --
CREATE USER 'admin_RRHH'@'localhost' IDENTIFIED BY 'AdminRRHH123';
GRANT ALL PRIVILEGES ON sistema_gestion.* TO 'admin_RRHH'@'localhost';


USE `gestion_empleados`;

-- Creacion de tablas --
CREATE TABLE `departamento` (
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `nombre`      VARCHAR(100) NOT NULL,
    `gerente_id`  INT          NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_departamento_nombre` (`nombre`),
    KEY `idx_departamento_gerente` (`gerente_id`)
) ENGINE = InnoDB;


CREATE TABLE `empleado` (
    `id`                     INT           NOT NULL AUTO_INCREMENT,
    `nombre`                 VARCHAR(100)  NOT NULL,
    `direccion`              VARCHAR(255)  NULL,
    `telefono`               VARCHAR(20)   NULL,
    `correo`                 VARCHAR(100)  NOT NULL,
    `fecha_inicio_contrato`  DATETIME      NOT NULL,
    `salario`                DECIMAL(12,2) NOT NULL,
    `departamento_id`        INT           NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_empleado_correo` (`correo`),
    KEY `idx_empleado_departamento` (`departamento_id`),
    CONSTRAINT `fk_empleado_departamento`
        FOREIGN KEY (`departamento_id`) REFERENCES `departamento` (`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB;


CREATE TABLE `gerente` (
    `empleado_id`          INT NOT NULL,
    `presupuesto_asignado` INT NOT NULL DEFAULT 0,
    `nivel_autorizacion`   INT NOT NULL DEFAULT 1,
    PRIMARY KEY (`empleado_id`),
    CONSTRAINT `fk_gerente_empleado`
        FOREIGN KEY (`empleado_id`) REFERENCES `empleado` (`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE = InnoDB;

ALTER TABLE `departamento`
    ADD CONSTRAINT `fk_departamento_gerente`
        FOREIGN KEY (`gerente_id`) REFERENCES `gerente` (`empleado_id`)
        ON UPDATE CASCADE
        ON DELETE SET NULL;


CREATE TABLE `proyecto` (
    `id`            INT          NOT NULL AUTO_INCREMENT,
    `nombre`        VARCHAR(100) NOT NULL,
    `descripcion`   VARCHAR(500) NULL,
    `fecha_inicio`  DATETIME     NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB;


CREATE TABLE `empleado_proyecto` (
    `empleado_id` INT NOT NULL,
    `proyecto_id` INT NOT NULL,
    PRIMARY KEY (`empleado_id`, `proyecto_id`),
    KEY `idx_ep_proyecto` (`proyecto_id`),
    CONSTRAINT `fk_ep_empleado`
        FOREIGN KEY (`empleado_id`) REFERENCES `empleado` (`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT `fk_ep_proyecto`
        FOREIGN KEY (`proyecto_id`) REFERENCES `proyecto` (`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE = InnoDB;


CREATE TABLE `registro_tiempo` (
    `id`                INT          NOT NULL AUTO_INCREMENT,
    `fecha`             DATETIME     NOT NULL,
    `horas_trabajadas`  INT          NOT NULL,
    `descripcion`       VARCHAR(500) NULL,
    `empleado_id`       INT          NOT NULL,
    `proyecto_id`       INT          NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_rt_empleado` (`empleado_id`),
    KEY `idx_rt_proyecto` (`proyecto_id`),
    CONSTRAINT `chk_rt_horas` CHECK (`horas_trabajadas` >= 0),
    CONSTRAINT `fk_rt_empleado`
        FOREIGN KEY (`empleado_id`) REFERENCES `empleado` (`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT `fk_rt_proyecto`
        FOREIGN KEY (`proyecto_id`) REFERENCES `proyecto` (`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB;