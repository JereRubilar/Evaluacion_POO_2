from abc import ABC, abstractmethod
from decimal import Decimal

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

class Gerente(Empleado):

    def __init__(self, presupuesto_asignado, nivel_autorizacion):
        self.presupuesto_asignado = presupuesto_asignado
        self.nivel_autorizacion = nivel_autorizacion

    def crear_departamento():
        pass

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

class Proyecto(ABC):

    def __init__(self, nombre, descripcion, fecha_inicio, empleados):
        self.nombre = nombre
        self.descripcion= descripcion
        self.fecha_inicio = fecha_inicio
        self.empleados = empleados

    def asignar_empleado():
        pass

    def desasignar_empleado():
        pass

class RegistroTiempo(ABC):

    def __init__(self, fecha, horas_trabajadas, descripcion, empleado, proyecto):
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion = descripcion
        self.empleado = empleado
        self.proyecto = proyecto
