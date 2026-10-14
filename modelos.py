from abc import ABC, abstractmethod


class Empleado(ABC):

    def __init__(self, nombre, direccion, telefono, correo, fecha_inicio_contrato, salario, empleado_id = None):
        self.id = empleado_id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario

    def validar(self):
        if not self.nombre or "@" not in self.correo:
            raise ValueError("nombre y correo válido son obligatorios.")

    def registrar_horas(self):
        pass

    def __str__(self):
        return f"[ID: {self.id}] Nombre: {self.nombre} - Dirección: {self.direccion} - Telefono {self.telefono} - Correo: {self.correo} - Salario: {self.salario} - Inicio de contrato: {self.fecha_inicio_contrato}\n"

class Gerente(Empleado):

    def __init__(self, nombre, direccion, telefono, correo, fecha_inicio_contrato, salario, presupuesto_asignado, nivel_autorizacion, empleado_id=None):
        super().__init__(nombre, direccion, telefono, correo, fecha_inicio_contrato, salario, empleado_id)
        self.presupuesto_asignado = presupuesto_asignado
        self.nivel_autorizacion = nivel_autorizacion

    def crear_departamento():
        pass

    def __str__(self):
        return f"[ID: {self.id}] Nombre: {self.nombre} - Dirección: {self.direccion} - Telefono {self.telefono} - Correo: {self.correo} - Salario: {self.salario} - Inicio de contrato: {self.fecha_inicio_contrato} - Presupuesto: {self.presupuesto_asignado} - Nivel de autorizacion: {self.nivel_autorizacion}\n"

class Departamento(ABC):

    def __init__(self, nombre, gerente, empleados, id = None):
        self.id = id
        self.nombre = nombre
        self.gerente = gerente
        self.empleados = empleados
        

    def asignar_empleado(self):
        pass

    def quitar_empleado():
        pass

    def cambiar_empleado():
        pass

    def __str__(self):
        return f"\n[ID: {self.id}] Nombre: {self.nombre} - Gerente: {self.gerente} - Empleados:"

class Proyecto(ABC):

    def __init__(self, nombre, descripcion, fecha_inicio, empleados = None, id = None):
        self.id = id
        self.nombre = nombre
        self.descripcion= descripcion
        self.fecha_inicio = fecha_inicio
        self.empleados = empleados if empleados is not None else []

    def asignar_empleado():
        pass

    def desasignar_empleado():
        pass

    def __str__(self):
        return f"\n[ID: {self.id}] Nombre: {self.nombre} - Descripción: {self.descripcion} - Fecha de inicio: {self.fecha_inicio}"

class RegistroTiempo(ABC):

    def __init__(self, fecha, horas_trabajadas, descripcion, empleado, proyecto, id = None):
        self.id = id
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion = descripcion
        self.empleado = empleado
        self.proyecto = proyecto

    def __str__(self):
        return f"[ID: {self.id}] Fecha: {self.fecha} - Horas_trabajadas: {self.horas_trabajadas} - Descripción: {self.descripcion} - Empleado: {self.empleado} - Proyecto: {self.proyecto}\n"