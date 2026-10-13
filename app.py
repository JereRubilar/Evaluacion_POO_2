from datetime import datetime

import mysql.connector
from modelos import Empleado, Gerente, Proyecto, RegistroTiempo
from repositorios import DepartamentoRepositorio, EmpleadoRepositorio, ProyectoRepositorio, RegistroTiempoRepositorio

def entero(mensaje):
    try:
        numero = int(input(mensaje))
    except ValueError as error:
        raise ValueError("Debe ingresar un número entero.") from error
    if numero < 1:
        raise ValueError("El número debe ser mayor que cero.")
    return numero

def decimal(mensaje):
    try:
        numero = float(input(mensaje).replace(",", "."))
    except ValueError as error:
        raise ValueError("Debe ingresar un número decimal.") from error
    if numero < 0:
        raise ValueError("El número no puede ser negativo.")
    return numero

def fecha(mensaje):
    try:
        return datetime.strptime(input(mensaje + " (AAAA-MM-DD): "), "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError as error:
        raise ValueError("Fecha inválida. Ejemplo: 2026-10-12.") from error

def texto(mensaje):
    valor = input(mensaje).strip()
    if not valor:
        raise ValueError("El campo no puede estar vacío.")
    return valor


# Empleados
def crear_empleado():
    tipo = input("Tipo E empleado o G gerente: ").upper()
    if tipo not in ("E", "G"):
        raise ValueError("Tipo de empleado inválido.")
    datos = (texto("Nombre: "), texto("Dirección: "), texto("Teléfono: "),
             texto("Correo: "), fecha("Inicio de contrato"), decimal("Salario: "))
    if tipo == "E":
        empleado = Empleado(*datos)
    else:
        empleado = Gerente(*datos, decimal("Presupuesto asignado: "),
                           entero("Nivel de autorización: "))
    EmpleadoRepositorio().crear(empleado)
    print("Empleado registrado con ID", empleado.id)

def listar_empleados():
    empleados = EmpleadoRepositorio().listar()
    if not empleados:
        print("No hay empleados registrados.")
    for empleado in empleados:
        print(empleado)

def eliminar_empleado():
    EmpleadoRepositorio().eliminar(entero("ID empleado: "))
    print("Empleado eliminado.")


# Departamentos
def crear_departamento():
    departamento = DepartamentoRepositorio().crear(texto("Nombre del departamento: "),
                                                   entero("ID del gerente a cargo: "))
    print("Departamento registrado con ID", departamento.id)

def asignar_a_departamento():
    DepartamentoRepositorio().asignar_empleado(entero("ID departamento: "),
                                               entero("ID empleado: "))
    print("Empleado asignado al departamento.")

def quitar_de_departamento():
    DepartamentoRepositorio().quitar_empleado(entero("ID departamento: "),
                                              entero("ID empleado: "))
    print("Empleado quitado del departamento.")

def cambiar_de_departamento():
    DepartamentoRepositorio().cambiar_empleado_dep(entero("ID empleado: "),
                                                   entero("ID departamento origen: "),
                                                   entero("ID departamento destino: "))
    print("Empleado movido de departamento.")

def listar_departamentos():
    repositorio = DepartamentoRepositorio()
    departamentos = repositorio.listar()
    if not departamentos:
        print("No hay departamentos registrados.")
    for departamento in departamentos:
        print(departamento)
        for empleado in repositorio.empleados_de(departamento.id):
            print("   -", empleado.nombre)


# Proyectos
def crear_proyecto():
    proyecto = Proyecto(texto("Nombre: "), texto("Descripción: "), fecha("Fecha de inicio"))
    ProyectoRepositorio().crear(proyecto)
    print("Proyecto creado con ID", proyecto.id)

def asignar_a_proyecto():
    ProyectoRepositorio().asignar_empleado(entero("ID proyecto: "), entero("ID empleado: "))
    print("Empleado asignado al proyecto.")

def desasignar_de_proyecto():
    ProyectoRepositorio().desasignar_empleado(entero("ID proyecto: "), entero("ID empleado: "))
    print("Empleado desasignado del proyecto.")

def listar_proyectos():
    repositorio = ProyectoRepositorio()
    horas = RegistroTiempoRepositorio()
    proyectos = repositorio.listar()
    if not proyectos:
        print("No hay proyectos registrados.")
    for proyecto in proyectos:
        print(proyecto, "|", horas.total_horas_proyecto(proyecto.id), "h")
        for empleado in repositorio.empleados_de(proyecto.id):
            print("   -", empleado.nombre)


# Registros de tiempo
def registrar_horas():
    registro = RegistroTiempo(fecha("Fecha"), decimal("Horas trabajadas: "),
                              texto("Descripción: "), entero("ID empleado: "),
                              entero("ID proyecto: "))
    RegistroTiempoRepositorio().registrar(registro)
    print("Horas registradas con ID", registro.id)

def ver_registros():
    registros = RegistroTiempoRepositorio().listar_por_empleado(entero("ID empleado: "))
    if not registros:
        print("El empleado no tiene registros.")
    for registro in registros:
        print(registro)


# Menú principal
OPCIONES = {
    "1": ("Crear empleado o gerente", crear_empleado),
    "2": ("Listar empleados", listar_empleados),
    "3": ("Eliminar empleado", eliminar_empleado),
    "4": ("Crear departamento", crear_departamento),
    "5": ("Asignar empleado a departamento", asignar_a_departamento),
    "6": ("Quitar empleado de departamento", quitar_de_departamento),
    "7": ("Cambiar empleado de departamento", cambiar_de_departamento),
    "8": ("Listar departamentos", listar_departamentos),
    "9": ("Crear proyecto", crear_proyecto),
    "10": ("Asignar empleado a proyecto", asignar_a_proyecto),
    "11": ("Desasignar empleado de proyecto", desasignar_de_proyecto),
    "12": ("Listar proyectos", listar_proyectos),
    "13": ("Registrar horas", registrar_horas),
    "14": ("Ver registros de un empleado", ver_registros),
}

def main():
    while True:
        print("\n===== GESTIÓN DE EMPRESA =====")
        for clave, (descripcion, _) in OPCIONES.items():
            print(f"{clave}) {descripcion}")
        print("0) Salir")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            break
        if opcion not in OPCIONES:
            print("Opción no válida.")
            continue
        try:
            OPCIONES[opcion][1]()
        except (ValueError, mysql.connector.Error) as error:
            print("No fue posible completar la operación:", error)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")