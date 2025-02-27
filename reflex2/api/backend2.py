import reflex as rx
from typing import Union, Optional
from sqlmodel import select, asc, desc, or_, func, cast, String, Field
from datetime import datetime, timedelta, time


def _get_percentage_change(
    value: Union[int, float], prev_value: Union[int, float]
) -> float:
    percentage_change = (
        round(((value - prev_value) / prev_value) * 100, 2)
        if prev_value != 0
        else 0.0
        if value == 0
        else float("inf")
    )
    return percentage_change

class AlertDialogState(rx.State):
    opened: bool = False

    @rx.event
    def dialog_open(self):
        self.opened = not self.opened


class RadioGroupNivelState(rx.State):
    radio_value: str = ""

class RadioGroupEstadoState(rx.State):
    radio_value: str = ""


class Registros(rx.Model, table=True):
    """Modelo para pacientes."""
    id: int = Field(default=None, primary_key=True)
    nombre: str
    especie:str
    motivo_hospitalizacion: str
    medico_id: str 
    tecnico_id: str
    examenes: Optional[str] = None 
    hora_examen: Optional[str] = None
    ayuno: Optional[str] = None
    via: Optional[str] = None
    procedimientos: Optional[str] = None
    observaciones: Optional[str] = None 
    alta: bool = False
    estado_paciente: str = "Estable"  # Valores posibles: Estable, Regular, Critico
    nivel_cuidados: str = "1.0" # Valores posibles: 1.0, 1.5, 2.0

class MonthValues(rx.Base):
    """Values for a month."""

    num_customers: int = 0
    total_payments: float = 0.0
    num_delivers: int = 0


class State(rx.State):
    """The app state."""

    dog_patients: list[Registros] = []
    cat_patients: list[Registros] = []
    sort_value: str = ""
    sort_reverse: bool = False
    search_value: str = ""
    show_alta: bool = False
    species_filter: str = ""  # ⚠ Nuevo filtro de especie
    current_register: Registros = Registros()

    # Values for current and previous month
    current_month_values: MonthValues = MonthValues()
    previous_month_values: MonthValues = MonthValues()


    def load_entries(self):
        self.load_entries_perro()
        self.load_entries_gato()

    def load_entries_perro(self) -> list[Registros]:
        """Obtiene todos los registros de la base de datos."""
        with rx.session() as session:

            query = select(Registros).where(Registros.especie == "Perro")


            if not self.show_alta: # Si no se muestra el Alta, entonces nos quedamos con los que no están de alta
                query = query.where(Registros.alta == False)  # Filtrar pacientes no dados de alta


            if self.search_value:
                search_value = f"%{self.search_value.lower()}%"
                query = query.where(
                    or_(
                        *[
                            getattr(Registros, field).ilike(search_value)
                            for field in Registros.get_fields()
                            if field not in ["id", "alta"]
                        ]
                    )
                )
            if self.sort_value:
                sort_column = getattr(Registros, self.sort_value)
                order = desc(sort_column) if self.sort_reverse else asc(sort_column)
                query = query.order_by(order)

            self.dog_patients = session.exec(query).all()
            

    def load_entries_gato(self) -> list[Registros]:
        """Obtiene todos los registros de la base de datos."""
        with rx.session() as session:

            query = select(Registros).where(Registros.especie == "Gato")

            if not self.show_alta: # Si no se muestra el Alta, entonces nos quedamos con los que no están de alta
                query = query.where(Registros.alta == False)  # Filtrar pacientes no dados de alta


            if self.search_value:
                search_value = f"%{self.search_value.lower()}%"
                query = query.where(
                    or_(
                        *[
                            getattr(Registros, field).ilike(search_value)
                            for field in Registros.get_fields()
                            if field not in ["id", "alta"]
                        ]
                    )
                )
            if self.sort_value:
                sort_column = getattr(Registros, self.sort_value)
                order = desc(sort_column) if self.sort_reverse else asc(sort_column)
                query = query.order_by(order)

            self.cat_patients = session.exec(query).all()

    @rx.event
    def set_species_filter(self, species: str):
        """Actualiza species_filter y recarga los registros"""
        self.species_filter = species
        self.load_entries_perro()  # Recargar los registros con la nueva especie
        self.load_entries_gato()  # Recargar los registros con la nueva especie

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries_perro()
        self.load_entries_gato()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries_perro()
        self.load_entries_gato()

    def check_alta(self):
        self.show_alta = not self.show_alta
        self.load_entries_perro()
        self.load_entries_gato()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries_perro()
        self.load_entries_gato()

    def get_register(self, register: Registros):
        self.current_register = register

    def add_register_to_db(self, form_data: dict):
        """Añade un nuevo registro a la base de datos."""
        with rx.session() as session:
            print(form_data)
            nuevo_registro = Registros(**form_data)
            session.add(nuevo_registro)
            session.commit()
        self.load_entries_perro()
        self.load_entries_gato()
        return rx.toast.info(
            f"Registros de {form_data['nombre']} añadido exitosamente.", position="bottom-right"
        )


    def update_register_to_db(self, form_data: dict):
        """Actualiza un registro existente en la base de datos."""
        with rx.session() as session:
            print(self.current_register.id)
            registro = session.exec(select(Registros).where(Registros.id == self.current_register.id)).first()
            if registro:
                for field, value in form_data.items():
                    print(field, value)
                    if hasattr(registro, field) and field != "id":
                        setattr(registro, field, value)
                session.add(registro)
                session.commit()
        self.load_entries_perro()
        self.load_entries_gato()
        return rx.toast.info(
            f"Registros de {form_data['nombre']} actualizado.", position="bottom-right"
        )


    def delete_register(self, id: int):
        """Elimina un registro de la base de datos."""
        with rx.session() as session:
            registro = session.exec(select(Registros).where(Registros.id == id)).first()
            if registro:
                session.delete(registro)
                session.commit()
        self.load_entries_perro()
        self.load_entries_gato()
        return rx.toast.info(f"Registros de {registro.nombre} eliminado.", position="bottom-right")


    dialog_patient_id: Optional[int] = None

    def update_alta(self, id: int):
        with rx.session() as session:
            registro = session.exec(select(Registros).where(Registros.id == id)).first()
            if registro:
                setattr(registro, "alta", True)
                paciente = getattr(registro, "nombre")
            session.commit()
        self.load_entries_perro()
        self.load_entries_gato()
        return rx.toast.info(f"{paciente} dado de alta.", position="bottom-right")

