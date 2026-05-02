from core import (
    CrudInterface,
    JsonManager,
    # JsonManagerError,
    LogMixin,
    ValidationMixin,
    ConfirmAction,
)
from models import Employee


class EmployeeController(CrudInterface, ValidationMixin, LogMixin, ConfirmAction):
    DATA_FILE = "data/Employee.json"

    def __init__(self):
        self.__storage = JsonManager(EmployeeController.DATA_FILE)

    def all(self):
        return self.__storage.load()
    
    def read(self):
        print("\n=== EMPLEADOS ===")        
        if not self.all():
            print("No hay clientes registrados")
            return
        for employee_data in self.all():
            employee = Employee.from_dict(employee_data)
            print(employee.display_name)

    def read_by_cedula(self, identification):
        employee = self.__storage.load()
        return next((e for e in employee if e["cedula"] == identification), None)

    def create(self):
        self.log_trace("Entrando a create()")

        name = self.validate_name(input("Ingrese nombre: "))
        identification = self.validate_identification(input("Ingrese cédula: "))
        salary = self.validate_salary(input("Ingrese sueldo: "))

        employee_data = self.__storage.load()

        # Validar unicidad de cédula
        if any(e["cedula"] == identification for e in employee_data):
            self.log_error("Ya existe un empleado con esa cédula")
            raise ValueError("Ya existe un empleado con esa cédula")

        if self.confirm_action("Guardar"):
            employee = Employee(name, identification, salary)
            id_new = self.__storage.append(employee.to_dict())

            self.log_success(f"Empleado creado con ID: {id_new}")
            return id_new

    def update(self):
        self.log_trace("Entrando a update()")

        identification = input("Ingrese cedula del empleado a actualizar: ")
        employee_data = self.read_by_cedula(identification)

        if not employee_data:
            self.log_error("Empleado no encontrado.")
            return

        id_employee = employee_data["id"]

        employee = Employee(
            employee_data["nombre"], employee_data["cedula"], employee_data["sueldo"]
        )

        options = {
            "1": (
                "Nombre",
                lambda: employee.name,
                lambda v: setattr(employee, "name", v),
                self.validate_name,
            ),
            "2": (
                "Cédula",
                lambda: employee.identification,
                lambda v: setattr(employee, "identification", v),
                self.validate_identification,
            ),
            "3": (
                "Sueldo",
                lambda: employee.salary,
                lambda v: setattr(employee, "salary", v),
                self.validate_salary,
            ),
        }

        while True:
            print("\n--- Datos actuales del empleado ---")
            for key, (label, getter, _, _) in options.items():
                print(f"{key}. {label}: {getter()}")
            print("4. Guardar cambios")
            print("5. Cancelar")

            option = input("Seleccione opción: ")

            if option in options:
                label, _, setter, validation = options[option]
                new_value = input(f"Ingrese nuevo {label}: ")
                setter(validation(new_value))
                self.log_info(f"{label} actualizado en memoria")
            elif option == "4":
                if self.confirm_action("Actualizar"):
                    data_employee = self.__storage.load()
                    for e in data_employee:
                        if (
                            e["cedula"] == employee.identification
                            and e["id"] != id_employee
                        ):
                            self.log_error("Ya existe otro empleado con esa cédula.")
                            break
                    else:
                        self.__storage.update(id_employee, employee.to_dict())
                        self.log_success("Cambios guardados correctamente.")
                        break
            elif option == "5":
                self.log_warn("Actualización cancelada por el usuario.")
                break
            else:
                self.log_warn("Opción inválida.")

    def delete(self):
        self.log_trace("Entrando a delete()")

        identification = input("Ingrese cedula del empleado a eliminar: ")
        employee_data = self.read_by_cedula(identification)

        if not employee_data:
            self.log_error("Empleado no encontrado.")
            return

        id_employee = employee_data["id"]

        empleado = Employee(
            employee_data["nombre"], employee_data["cedula"], employee_data["sueldo"]
        )

        data = {
            "Nombre": lambda: empleado.name,
            "Cédula": lambda: empleado.identification,
            "Sueldo": lambda: empleado.salary,
        }

        while True:
            print("\n--- Datos actuales del empleado ---")
            for label, getter in data.items():
                print(f"{label}: {getter()}")
            print("\n4. Eliminar")
            print("5. Cancelar")

            opcion = input("Seleccione opción: ")

            if opcion == "4":
                if self.confirm_action("Eliminar"):
                    self.__storage.delete(id_employee)
                    self.log_success("Empleado eliminado correctamente.")
                    break
            elif opcion == "5":
                self.log_warn("Eliminación cancelada por el usuario.")
                break
            else:
                self.log_warn("Opción inválida.")
