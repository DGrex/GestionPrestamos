"""
IMPLEMENTACIÓN DE CONSULTAS Y ESTADÍSTICAS
Este archivo contiene las funciones necesarias para completar el proyecto.
Copiar estas funciones en menuBill.py en los lugares indicados.
"""

# ==================== CONSULTAS ====================


def consultar_empleado():
    """Consultar un empleado por cédula"""
    from models.empleado_crud import EmpleadoCRUD
    from decorators import decorator_menu

    cedula = input("Ingrese la cédula del empleado: ")
    crud_emp = EmpleadoCRUD()

    try:
        empleado = crud_emp.read_by_cedula(cedula)
        if empleado:
            print("\n========================================")
            print("           DATOS DEL EMPLEADO")
            print("========================================")
            print(f"ID: {empleado['id']}")
            print(f"Nombre: {empleado['nombre']}")
            print(f"Cédula: {empleado['cedula']}")
            print(f"Sueldo: ${empleado['sueldo']:,.2f}")
            print("========================================\n")
        else:
            print("❌ Empleado no encontrado.")
    except Exception as e:
        print(f"❌ Error al consultar: {e}")


def consultar_prestamo():
    """Consultar un préstamo por ID"""
    from models.prestamo_crud import PrestamoCRUD
    from models.empleado_crud import EmpleadoCRUD

    prestamo_id = input("Ingrese el ID del préstamo: ")
    crud_pres = PrestamoCRUD()
    crud_emp = EmpleadoCRUD()

    try:
        prestamo = crud_pres.read(int(prestamo_id))
        if prestamo:
            empleado = crud_emp.read(prestamo["empleado_id"])
            print("\n========================================")
            print("           DATOS DEL PRÉSTAMO")
            print("========================================")
            print(f"ID: {prestamo['id']}")
            print(f"Empleado: {empleado['nombre']}")
            print(f"Fecha: {prestamo['fecha_prestamo']}")
            print(f"Monto: ${prestamo['monto']:,.2f}")
            print(f"Cuotas: {prestamo['numero_cuotas']}")
            print(f"Cuota: ${prestamo['cuota']:,.2f}")
            print(f"Saldo: ${prestamo['saldo']:,.2f}")
            print(f"Estado: {prestamo['estado'].upper()}")
            print("========================================\n")
        else:
            print("❌ Préstamo no encontrado.")
    except ValueError:
        print("❌ ID inválido.")
    except Exception as e:
        print(f"❌ Error al consultar: {e}")


def consultar_pago():
    """Consultar un pago por ID"""
    from models.pago_crud import PagoCRUD
    from models.prestamo_crud import PrestamoCRUD

    pago_id = input("Ingrese el ID del pago: ")
    crud_pago = PagoCRUD()
    crud_pres = PrestamoCRUD()

    try:
        pago = crud_pago.read(int(pago_id))
        if pago:
            prestamo = crud_pres.read(pago["prestamo_id"])
            print("\n========================================")
            print("           DATOS DEL PAGO")
            print("========================================")
            print(f"ID: {pago['id']}")
            print(f"ID Préstamo: {pago['prestamo_id']}")
            print(f"Monto Préstamo: ${prestamo['monto']:,.2f}")
            print(f"Fecha Pago: {pago['fecha_pago']}")
            print(f"Valor Pago: ${pago['valor_pago']:,.2f}")
            print("========================================\n")
        else:
            print("❌ Pago no encontrado.")
    except ValueError:
        print("❌ ID inválido.")
    except Exception as e:
        print(f"❌ Error al consultar: {e}")


# ==================== ESTADÍSTICAS ====================


class EstadisticasService:
    """Servicio para calcular estadísticas del sistema"""

    def __init__(self):
        from models.prestamo_crud import PrestamoCRUD
        from models.pago_crud import PagoCRUD

        self.crud_prestamos = PrestamoCRUD()
        self.crud_pagos = PagoCRUD()

    def obtener_estadisticas(self):
        """Calcular todas las estadísticas necesarias"""
        prestamos = self.crud_prestamos.all()
        pagos = self.crud_pagos.all()

        if not prestamos:
            return None

        montos = [p["monto"] for p in prestamos]
        saldos = [p["saldo"] for p in prestamos]

        estadisticas = {
            "total_prestamos": len(prestamos),
            "total_pagos": len(pagos),
            "monto_total": sum(montos),
            "promedio": sum(montos) / len(montos) if montos else 0,
            "maximo": max(montos) if montos else 0,
            "minimo": min(montos) if montos else 0,
            "pendientes": len([p for p in prestamos if p["estado"] == "pendiente"]),
            "pagados": len([p for p in prestamos if p["estado"] == "pagado"]),
            "saldo_total_pendiente": sum(saldos),
        }

        return estadisticas

    def mostrar_estadisticas(self):
        """Mostrar estadísticas formateadas"""
        stats = self.obtener_estadisticas()

        if not stats:
            print("❌ No hay préstamos registrados.")
            return

        print("\n========================================")
        print("           ESTADÍSTICAS")
        print("========================================")
        print(f"Total de préstamos: {stats['total_prestamos']}")
        print(f"Total de pagos: {stats['total_pagos']}")
        print(f"Monto total: ${stats['monto_total']:,.2f}")
        print(f"Promedio: ${stats['promedio']:,.2f}")
        print(f"Máximo: ${stats['maximo']:,.2f}")
        print(f"Mínimo: ${stats['minimo']:,.2f}")
        print(f"Pendientes: {stats['pendientes']}")
        print(f"Pagados: {stats['pagados']}")
        print(f"Saldo total pendiente: ${stats['saldo_total_pendiente']:,.2f}")
        print("========================================\n")


def ver_estadisticas():
    """Función llamada desde el menú"""
    servicio = EstadisticasService()
    servicio.mostrar_estadisticas()


# ==================== CÓMO USAR ====================

"""
INSTRUCCIONES DE INTEGRACIÓN:

1. En menuBill.py, reemplaza la función query_menu() con:

def query_menu():
    show_menu(
        "Menú Consultas",
        [
            {"label": "Consultar Empleado", "action": consultar_empleado},
            {"label": "Consultar Préstamo", "action": consultar_prestamo},
            {"label": "Consultar Pago", "action": consultar_pago},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )

2. En menuBill.py, reemplaza la función statistics_menu() con:

def statistics_menu():
    show_menu(
        "Menú Estadísticas",
        [
            {"label": "Ver estadísticas", "action": ver_estadisticas},
            {"label": "Atrás", "action": "break"},
            {"label": "Salir", "action": "exit"},
        ],
    )

3. Agrega estas funciones al final de menuBill.py o en un archivo separado stats.py

4. Importa las funciones en menuBill.py
"""
