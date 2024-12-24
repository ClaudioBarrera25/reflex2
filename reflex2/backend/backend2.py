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




class Registros(rx.Model, table=True):
    """Modelo para pacientes."""
    id: int = Field(default=None, primary_key=True)
    nombre: str
    motivo_hospitalizacion: str
    medico_id: str 
    tecnico_id: str
    examenes: Optional[str] = None 
    hora_examen: Optional[str] = None
    ayuno: Optional[str] = None
    via: Optional[str] = None
    procedimientos: Optional[str] = None
    observaciones: Optional[str] = None 
    alta: bool


class MonthValues(rx.Base):
    """Values for a month."""

    num_customers: int = 0
    total_payments: float = 0.0
    num_delivers: int = 0


class State(rx.State):
    """The app state."""

    patients: list[Registros] = []
    sort_value: str = ""
    sort_reverse: bool = False
    search_value: str = ""
    current_register: Registros = Registros()
    # Values for current and previous month
    current_month_values: MonthValues = MonthValues()
    previous_month_values: MonthValues = MonthValues()

    def load_entries(self) -> list[Registros]:
        """Obtiene todos los registros de la base de datos."""
        with rx.session() as session:
            query = select(Registros)
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
            self.users = session.exec(query).all()


        self.get_current_month_values()
        self.get_previous_month_values()

    

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def get_register(self, register: Registros):
        self.current_register = register

    def add_register_to_db(self, form_data: dict):
        """Añade un nuevo registro a la base de datos."""
        with rx.session() as session:
            nuevo_registro = Registros(**form_data)
            session.add(nuevo_registro)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Registros de {form_data['nombre']} añadido exitosamente.", position="bottom-right"
        )


    def update_register_to_db(self, form_data: dict):
        """Actualiza un registro existente en la base de datos."""
        with rx.session() as session:
            registro = session.exec(select(Registros).where(Registros.id == self.current_register.id)).first()
            if registro:
                for field, value in form_data.items():
                    if hasattr(registro, field) and field != "id":
                        setattr(registro, field, value)
                session.add(registro)
                session.commit()
        self.load_entries()
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
        self.load_entries()
        return rx.toast.info(f"Registros de {registro.nombre} eliminado.", position="bottom-right")


