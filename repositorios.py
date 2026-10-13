from modelos import *
# from conexiones import conexion


class RegistroDAO:
    def buscar_empleado(self, empleado_id):
        sql = "SELECT id,nombre,direccion,telefono,correo,fecha_inicio_contrato,salario FROM empleados WHERE id=%s"
        with conexion() as cn:
            cur = cn.cursor()
            try:
                cur.execute(sql, (empleado_id)); f = cur.fetchone()
                return Empleado(f[1], f[2], f[3], f[4], f[5], f[6], f[0]) if f else None
            finally: cur.close()

    def buscar_departamento(self, departamento_id):
        sql = "SELECT id,nombre,gerente FROM departamento WHERE id=%s"
        with conexion() as cn:
            cur = cn.cursor()
            try:
                cur.execute(sql, (departamento_id)); f = cur.fetchone()
                return Departamento(f[1], f[2], f[0]) if f else None
            finally: cur.close()

    def listar_departamento(self, departamento_id):
        sql = "SELECT nombre, correo, telefono FROM empleados WHERE id_departamento=%s"
        with conexion as cn:
            cur = cn.cursor()
            try:
                cur.execute(sql, (departamento_id)); f = cur.fetchone()
                return Empleado(f[1], f[2], f[3], f[0]) if f else None
            finally: cur.close()

    