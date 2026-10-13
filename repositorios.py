from modelos import Empleado, Gerente, Departamento, Proyecto, RegistroTiempo
from conexiones import conexion

class EmpleadoRepositorio:
    def crear(self, empleado):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql_empleado = """
                    INSERT INTO empleado (nombre, direccion, telefono, correo, fecha_inicio_contrato, salario, departamento_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                departamento_id = getattr(empleado, 'departamento_id', 1)
                
                cur.execute(sql_empleado, (
                    empleado.nombre,
                    empleado.direccion,
                    empleado.telefono,
                    empleado.correo,
                    empleado.fecha_inicio_contrato,
                    empleado.salario,
                    departamento_id
                ))
                empleado.id = cur.lastrowid

                if isinstance(empleado, Gerente):
                    sql_gerente = """
                        INSERT INTO gerente (empleado_id, presupuesto_asignado, nivel_autorizacion)
                        VALUES (%s, %s, %s)
                    """
                    cur.execute(sql_gerente, (
                        empleado.id,
                        empleado.presupuesto_asignado,
                        empleado.nivel_autorizacion
                    ))
                cn.commit()
            except Exception as e:
                cn.rollback()
                raise e
            finally:
                cur.close()

    def listar(self):
        sql = """
            SELECT e.id, e.nombre, e.direccion, e.telefono, e.correo, e.fecha_inicio_contrato, e.salario,
            g.presupuesto_asignado, g.nivel_autorizacion
            FROM empleado e
            LEFT JOIN gerente g ON e.id = g.empleado_id
        """
        with conexion() as cn:
            cur = cn.cursor()
            try:
                cur.execute(f"SELECT {sql}")
                filas = cur.fetchall()
                resultado = []
                for f in filas:
                    if f[7] is not None:
                        emp = Gerente(f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[0])
                    else:
                        emp = Empleado(f[1], f[2], f[3], f[4], f[5], f[6], f[0])
                    resultado.append(emp)
                return resultado
            finally:
                cur.close()

    def eliminar(self, empleado_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                cur.execute("DELETE FROM empleado WHERE id = %s", (empleado_id,))
                cn.commit()
            except Exception as e:
                cn.rollback()
                raise e
            finally:
                cur.close()


class DepartamentoRepositorio:
    def crear(self, nombre, gerente_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = "INSERT INTO departamento (nombre, gerente_id) VALUES (%s, %s)"
                cur.execute(sql, (nombre, gerente_id if gerente_id else None))
                cn.commit()
                dep_id = cur.lastrowid
                return Departamento(nombre, gerente_id, [], dep_id)
            except Exception as e:
                cn.rollback()
                raise e
            finally:
                cur.close()

    def listar(self):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                cur.execute("SELECT id, nombre, gerente_id FROM departamento")
                filas = cur.fetchall()
                return [Departamento(f[1], f[2], [], f[0]) for f in filas]
            finally:
                cur.close()

    def empleados_de(self, departamento_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = "SELECT id, nombre, direccion, telefono, correo, fecha_inicio_contrato, salario FROM empleado WHERE departamento_id = %s"
                cur.execute(sql, (departamento_id,))
                filas = cur.fetchall()
                return [Empleado(f[1], f[2], f[3], f[4], f[5], f[6], f[0]) for f in filas]
            finally:
                cur.close()

    def asignar_empleado(self, departamento_id, empleado_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = "UPDATE empleado SET departamento_id = %s WHERE id = %s"
                cur.execute(sql, (departamento_id, empleado_id))
                cn.commit()
            except Exception as e:
                cn.rollback()
                raise e
            finally:
                cur.close()

    def quitar_empleado(self, departamento_id, empleado_id):
        self.asignar_empleado(None, empleado_id)

    def cambiar_empleado_dep(self, empleado_id, dep_origen_id, dep_destino_id):
        self.asignar_empleado(dep_destino_id, empleado_id)


class ProyectoRepositorio:
    def crear(self, proyecto):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = "INSERT INTO proyecto (nombre, descripcion, fecha_inicio) VALUES (%s, %s, %s)"
                cur.execute(sql, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio))
                cn.commit()
                proyecto.id = cur.lastrowid
            except Exception as e:
                cn.rollback()
                raise e
            finally:
                cur.close()

    def listar(self):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                cur.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyecto")
                filas = cur.fetchall()
                return [Proyecto(f[1], f[2], f[3], [], f[0]) for f in filas]
            finally:
                cur.close()

    def empleados_de(self, proyecto_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = """
                    SELECT e.id, e.nombre, e.direccion, e.telefono, e.correo, e.fecha_inicio_contrato, e.salario 
                    FROM empleado e
                    JOIN empleado_proyecto ep ON e.id = ep.empleado_id
                    WHERE ep.proyecto_id = %s
                """
                cur.execute(sql, (proyecto_id,))
                filas = cur.fetchall()
                return [Empleado(f[1], f[2], f[3], f[4], f[5], f[6], f[0]) for f in filas]
            finally:
                cur.close()

    def asignar_empleado(self, proyecto_id, empleado_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = "INSERT IGNORE INTO empleado_proyecto (empleado_id, proyecto_id) VALUES (%s, %s)"
                cur.execute(sql, (empleado_id, proyecto_id))
                cn.commit()
            except Exception as e:
                cn.rollback()
                raise e
            finally:
                cur.close()

    def desasignar_empleado(self, proyecto_id, empleado_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = "DELETE FROM empleado_proyecto WHERE empleado_id = %s AND proyecto_id = %s"
                cur.execute(sql, (empleado_id, proyecto_id))
                cn.commit()
            except Exception as e:
                cn.rollback()
                raise e
            finally:
                cur.close()


class RegistroTiempoRepositorio:
    def registrar(self, registro):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = """
                    INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion, empleado_id, proyecto_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cur.execute(sql, (
                    registro.fecha,
                    registro.horas_trabajadas,
                    registro.descripcion,
                    registro.empleado,  # ID del empleado
                    registro.proyecto   # ID del proyecto
                ))
                cn.commit()
                registro.id = cur.lastrowid
            except Exception as e:
                cn.rollback()
                raise e
            finally:
                cur.close()

    def listar_por_empleado(self, empleado_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = "SELECT id, fecha, horas_trabajadas, descripcion, empleado_id, proyecto_id FROM registro_tiempo WHERE empleado_id = %s"
                cur.execute(sql, (empleado_id,))
                filas = cur.fetchall()
                return [RegistroTiempo(f[1], f[2], f[3], f[4], f[5], f[0]) for f in filas]
            finally:
                cur.close()

    def total_horas_proyecto(self, proyecto_id):
        with conexion() as cn:
            cur = cn.cursor()
            try:
                sql = "SELECT SUM(horas_trabajadas) FROM registro_tiempo WHERE proyecto_id = %s"
                cur.execute(sql, (proyecto_id,))
                fila = cur.fetchone()
                return fila[0] if fila and fila[0] is not None else 0
            finally:
                cur.close()