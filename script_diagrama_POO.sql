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

-- ==========================================
-- 1. INSERTAR DEPARTAMENTOS (Se insertan primero sin gerente_id para evitar conflictos circulares)
-- ==========================================
INSERT INTO `departamento` (`id`, `nombre`, `gerente_id`) VALUES
(1, 'Desarrollo de Software', NULL),
(2, 'Recursos Humanos', NULL),
(3, 'Infraestructura y Redes', NULL);


-- ==========================================
-- 2. INSERTAR EMPLEADOS (Incluyendo empleados normales y futuros gerentes)
-- ==========================================
INSERT INTO `empleado` (`id`, `nombre`, `direccion`, `telefono`, `correo`, `fecha_inicio_contrato`, `salario`, `departamento_id`) VALUES
(1, 'Carlos Pérez', 'Av. Libertador 123', '+56911112222', 'carlos.perez@empresa.com', '2025-01-15 09:00:00', 1200000.00, 1),
(2, 'Ana Gómez', 'Calle Los Alerces 456', '+56933334444', 'ana.gomez@empresa.com', '2025-03-01 09:00:00', 950000.00, 2),
(3, 'Luis Soto', 'Pasaje Los Aromos 789', '+56955556666', 'luis.soto@empresa.com', '2025-06-10 09:00:00', 1100000.00, 3),
(4, 'María Silva', 'San Martín 321', '+56977778888', 'maria.silva@empresa.com', '2024-11-20 09:00:00', 1800000.00, 1),
(5, 'Jorge Rivas', 'Pedro de Valdivia 999', '+56999990000', 'jorge.rivas@empresa.com', '2024-08-01 09:00:00', 1700000.00, 3);

-- ==========================================
-- 3. INSERTAR GERENTES (Heredan de los empleados con IDs 4 y 5)
-- ==========================================
INSERT INTO `gerente` (`empleado_id`, `presupuesto_asignado`, `nivel_autorizacion`) VALUES
(4, 5000000, 3),
(5, 3500000, 2);

-- (Opcional) Si quieres un tercer gerente, puedes registrar otro empleado y asignarlo aquí. 
-- Para este ejemplo, dejaremos a Ana Gómez (ID 2) sin rol de gerente o podemos actualizar un departamento.


-- ==========================================
-- 4. ACTUALIZAR DEPARTAMENTOS CON SUS GERENTES
-- ==========================================
UPDATE `departamento` SET `gerente_id` = 4 WHERE `id` = 1;
UPDATE `departamento` SET `gerente_id` = 5 WHERE `id` = 3;
-- El departamento 2 (Recursos Humanos) se queda con gerente_id NULL para probar valores nulos.


-- ==========================================
-- 5. INSERTAR PROYECTOS
-- ==========================================
INSERT INTO `proyecto` (`id`, `nombre`, `descripcion`, `fecha_inicio`) VALUES
(1, 'Plataforma E-Commerce', 'Desarrollo de tienda online B2C con pasarela de pago', '2026-03-01 08:00:00'),
(2, 'Migración Cloud', 'Migración de servidores físicos a infraestructura AWS', '2026-04-15 08:00:00'),
(3, 'Portal de Clientes', 'Rediseño de interfaz de usuario y panel de autogestión', '2026-05-10 08:00:00');


-- ==========================================
-- 6. ASIGNAR EMPLEADOS A PROYECTOS (Tabla intermedia empleado_proyecto)
-- ==========================================
INSERT INTO `empleado_proyecto` (`empleado_id`, `proyecto_id`) VALUES
(1, 1), -- Carlos Pérez en E-Commerce
(2, 3), -- Ana Gómez en Portal de Clientes
(3, 2), -- Luis Soto en Migración Cloud
(4, 1), -- María Silva en E-Commerce
(5, 2); -- Jorge Rivas en Migración Cloud

-- ==========================================
-- 7. INSERTAR REGISTROS DE TIEMPO
-- ==========================================
INSERT INTO `registro_tiempo` (`id`, `fecha`, `horas_trabajadas`, `descripcion`, `empleado_id`, `proyecto_id`) VALUES
(1, '2026-10-01 10:00:00', 8, 'Configuración inicial del repositorio y base de datos', 1, 1),
(2, '2026-10-02 11:30:00', 6, 'Definición de políticas de seguridad y accesos IAM', 3, 2),
(3, '2026-10-03 15:00:00', 7, 'Diseño de flujos de usuario para la interfaz web', 2, 3);