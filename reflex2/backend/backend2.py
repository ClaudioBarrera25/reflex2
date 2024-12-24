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




class Registro(rx.Model, table=True):
    """Modelo para pacientes."""
    id: int = Field(default=None, primary_key=True)
    nombre: str
    motivo_hospitalizacion: str
    medico_id: str 
    tecnico_id: str
    examenes: Optional[str] = None 
    hora_examen: Optional[datetime] = None
    ayuno: Optional[time] = None
    via: Optional[datetime] = None
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

    users: list[Registro] = []
    sort_value: str = ""
    sort_reverse: bool = False
    search_value: str = ""
    current_register: Registro = Registro()
    # Values for current and previous month
    current_month_values: MonthValues = MonthValues()
    previous_month_values: MonthValues = MonthValues()

    def load_entries(self) -> list[Registro]:
        """Obtiene todos los registros de la base de datos."""
        with rx.session() as session:
            query = select(Registro)
            if self.search_value:
                search_value = f"%{self.search_value.lower()}%"
                query = query.where(
                    or_(
                        *[
                            getattr(Registro, field).ilike(search_value)
                            for field in Registro.get_fields()
                            if field not in ["id", "alta"]
                        ]
                    )
                )
            if self.sort_value:
                sort_column = getattr(Registro, self.sort_value)
                order = desc(sort_column) if self.sort_reverse else asc(sort_column)
                query = query.order_by(order)
            self.users = session.exec(query).all()


        self.get_current_month_values()
        self.get_previous_month_values()

    
    # def get_current_month_values(self):
    #     """Calculate current month's values."""
    #     now = datetime.now()
    #     start_of_month = datetime(now.year, now.month, 1)

    #     current_month_users = [
    #         user
    #         for user in self.users
    #         if datetime.strptime(user.date, "%Y-%m-%d %H:%M:%S") >= start_of_month
    #     ]
    #     num_customers = len(current_month_users)
    #     total_payments = sum(user.payments for user in current_month_users)
    #     num_delivers = len(
    #         [user for user in current_month_users if user.status == "Delivered"]
    #     )
    #     self.current_month_values = MonthValues(
    #         num_customers=num_customers,
    #         total_payments=total_payments,
    #         num_delivers=num_delivers,
    #     )

    # def get_previous_month_values(self):
    #     """Calculate previous month's values."""
    #     now = datetime.now()
    #     first_day_of_current_month = datetime(now.year, now.month, 1)
    #     last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    #     start_of_last_month = datetime(
    #         last_day_of_last_month.year, last_day_of_last_month.month, 1
    #     )

    #     previous_month_users = [
    #         user
    #         for user in self.users
    #         if start_of_last_month
    #         <= datetime.strptime(user.date, "%Y-%m-%d %H:%M:%S")
    #         <= last_day_of_last_month
    #     ]
    #     # We add some dummy values to simulate growth/decline. Remove them in production.
    #     num_customers = len(previous_month_users) + 3
    #     total_payments = sum(user.payments for user in previous_month_users) + 240
    #     num_delivers = (
    #         len([user for user in previous_month_users if user.status == "Delivered"])
    #         + 5
    #     )

    #     self.previous_month_values = MonthValues(
    #         num_customers=num_customers,
    #         total_payments=total_payments,
    #         num_delivers=num_delivers,
    #     )

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def get_user(self, user: Registro):
        self.current_register = user

    def update_register_to_db(self, form_data: dict):
        """Actualiza un registro existente en la base de datos."""
        with rx.session() as session:
            registro = session.exec(select(Registro).where(Registro.id == self.current_register.id)).first()
            if registro:
                for field, value in form_data.items():
                    if hasattr(registro, field) and field != "id":
                        setattr(registro, field, value)
                session.add(registro)
                session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Registro de {form_data['nombre']} actualizado.", position="bottom-right"
        )

    def update_register_to_db(self, form_data: dict):
        """Actualiza un registro existente en la base de datos."""
        with rx.session() as session:
            registro = session.exec(select(Registro).where(Registro.id == self.current_register.id)).first()
            if registro:
                for field, value in form_data.items():
                    if hasattr(registro, field) and field != "id":
                        setattr(registro, field, value)
                session.add(registro)
                session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Registro de {form_data['nombre']} actualizado.", position="bottom-right"
        )


    def delete_register(self, id: int):
        """Elimina un registro de la base de datos."""
        with rx.session() as session:
            registro = session.exec(select(Registro).where(Registro.id == id)).first()
            if registro:
                session.delete(registro)
                session.commit()
        self.load_entries()
        return rx.toast.info(f"Registro de {registro.nombre} eliminado.", position="bottom-right")

    # @rx.var(cache=True)
    # def payments_change(self) -> float:
    #     return _get_percentage_change(
    #         self.current_month_values.total_payments,
    #         self.previous_month_values.total_payments,
    #     )

    # @rx.var(cache=True)
    # def customers_change(self) -> float:
    #     return _get_percentage_change(
    #         self.current_month_values.num_customers,
    #         self.previous_month_values.num_customers,
    #     )

    # @rx.var(cache=True)
    # def delivers_change(self) -> float:
    #     return _get_percentage_change(
    #         self.current_month_values.num_delivers,
    #         self.previous_month_values.num_delivers,
    #     )
