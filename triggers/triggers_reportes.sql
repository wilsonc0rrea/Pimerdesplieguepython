DELIMITER $$

USE `pythonreports`$$

-- Trigger para INSERT
DROP TRIGGER IF EXISTS `trg_reporteshistorial_insert`$$
CREATE TRIGGER `trg_reporteshistorial_insert`
AFTER INSERT ON `reportes`
FOR EACH ROW
BEGIN
    INSERT INTO reportes_historial (
        serial_id, seriales, vin, motor, trabajo_id, precio, empleado_id, cliente_id,
        created_at, updated_at, fecha_servicio, flag, estado_id, observacion,
        usuario_id, updated_usuario_id,
	accion
    ) VALUES (
        NEW.serial_id, NEW.seriales, NEW.vin, NEW.motor, NEW.trabajo_id, NEW.precio, NEW.empleado_id, NEW.cliente_id,
        NEW.created_at, NEW.updated_at, NEW.fecha_servicio, NEW.flag, NEW.estado_id, NEW.observacion,
        NEW.usuario_id, NEW.updated_usuario_id,
	'INSERT'
    );
END$$

-- Trigger para UPDATE
DROP TRIGGER IF EXISTS `trg_reporteshistorial_update`$$
CREATE TRIGGER `trg_reporteshistorial_update`
AFTER UPDATE ON `reportes`
FOR EACH ROW
BEGIN
    INSERT INTO reportes_historial (
        serial_id, seriales, vin, motor, trabajo_id, precio, empleado_id, cliente_id,
        created_at, updated_at, fecha_servicio, flag, estado_id, observacion,
        usuario_id, updated_usuario_id,
	accion
    ) VALUES (
        OLD.serial_id, OLD.seriales, OLD.vin, OLD.motor, OLD.trabajo_id, OLD.precio, OLD.empleado_id, OLD.cliente_id,
        OLD.created_at, OLD.updated_at, OLD.fecha_servicio, OLD.flag, OLD.estado_id, OLD.observacion,
        OLD.usuario_id, OLD.updated_usuario_id,
	'UPDATE'
    );
END$$

-- Trigger para DELETE
DROP TRIGGER IF EXISTS `trg_reporteshistorial_delete`$$
CREATE TRIGGER `trg_reporteshistorial_delete`
AFTER DELETE ON `reportes`
FOR EACH ROW
BEGIN
    INSERT INTO reportes_historial (
        serial_id, seriales, vin, motor, trabajo_id, precio, empleado_id, cliente_id,
        created_at, updated_at, fecha_servicio, flag, estado_id, observacion,
        usuario_id, updated_usuario_id,
	accion
    ) VALUES (
        OLD.serial_id, OLD.seriales, OLD.vin, OLD.motor, OLD.trabajo_id, OLD.precio, OLD.empleado_id, OLD.cliente_id,
        OLD.created_at, OLD.updated_at, OLD.fecha_servicio, OLD.flag, OLD.estado_id, OLD.observacion,
        OLD.usuario_id, OLD.updated_usuario_id,
	'DELETE'
    );
END$$

DELIMITER ;