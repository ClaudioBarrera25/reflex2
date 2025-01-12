import reflex as rx
from ..backend.backend2 import State, Registros, AlertDialogState
from ..components.form_field import form_field, form_field_radio
from ..components.status_badges import status_badge


def alta_dialog(patient: Registros):
    """Dialog box para confirmar el alta de un paciente."""
    return \
    rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(
                rx.icon("stethoscope"), "Alta"
            )
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Confirmar Alta"),
            rx.alert_dialog.description(
                f"¿Estás seguro que deseas dar de alta al paciente {patient.nombre}?"
            ),
            rx.hstack(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancelar",
                        color_scheme="red"
                    )
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Confirmar",
                        on_click=lambda: State.update_alta(getattr(patient, "id")),
                        color_scheme="green"
                    ),
                ),
            )
        ),
    )


def show_patient(patient: Registros):
    estado_color = {
        "Estable": "green",
        "Regular": "yellow",
        "Critico": "red",
    }
    print(f"{patient.tecnico_id}")
    """Show a patient in a table row."""
    return rx.table.row(
        rx.table.cell(patient.nombre),
        rx.table.cell(patient.motivo_hospitalizacion),
        rx.table.cell(patient.medico_id),
        rx.table.cell(patient.tecnico_id),
        rx.table.cell(
            rx.match(
                patient.estado_paciente,
                ("Estable", rx.text("Estable", color="green", font_weight="bold")),
                ("Regular", rx.text("Regular", color="yellow", font_weight="bold")),
                ("Critico", rx.text("Critico", color="red", font_weight="bold")),
                rx.text("Pendiente", color="white", font_weight="bold")
            )
        ),
        rx.table.cell(
            rx.text(
                patient.nivel_cuidados,
                font_weight="bold",
            )
        ),
        rx.table.cell(patient.examenes),
        rx.table.cell(patient.hora_examen),
        rx.table.cell(patient.ayuno),
        rx.table.cell(patient.via),
        rx.table.cell(patient.procedimientos),
        rx.table.cell(patient.observaciones),
        rx.table.cell(
            rx.hstack(
                update_patient_dialog(patient),
                alta_dialog(patient),# Nuevo campo: Botón para dar de alta al paciente
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    on_click=lambda: State.delete_register(getattr(patient, "id")),
                    size="2",
                    variant="solid",
                    color_scheme="red",
                ),
            )
        ),
        
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def add_patient_button() -> rx.Component:
    """Button and form to add a new patient."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Añadir paciente", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="user-plus", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title("Add New Patient", weight="bold", margin="0"),
                    rx.dialog.description("Fill the form with the patient's info"),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        form_field("Name", "Nombre Paciente", "text", "nombre", "paw-print"),
                        form_field(
                            "Motivo de Hospitalización",
                            "Motivo de Hospitalización",
                            "text",
                            "motivo_hospitalizacion",
                            "clipboard",
                        ),
                        form_field(
                            "Médico",
                            "Nombre Médico",
                            "text",
                            "medico_id",
                            "user",
                        ),
                        form_field(
                            "Técnico",
                            "Nombre Técnico",
                            "text",
                            "tecnico_id",
                            "user",
                        ),
                        form_field_radio(
                            "Estado",
                            "Estado Paciente",
                            "radio",
                            "via",
                            "heart",
                            ["Estable", "Regular", "Critico"]
                        ),
                        form_field_radio(
                            "Prioridad",
                            "Nivel de cuidados",
                            "radio",
                            "via",
                            "shield",
                            ["1.0", "1.5", "2.0"]
                        ),
                        form_field(
                            "Exámenes",
                            "Exámenes paciente",
                            "text",
                            "examenes",
                            "syringe",
                        ),
                        form_field(
                            "Hora de Examen",
                            "Hora de Examen",
                            "datetime-local",
                            "hora_examen",
                            "clock",
                        ),
                        form_field(
                            "Ayuno",
                            "Hora Inicio Ayuno",
                            "time",
                            "ayuno",
                            "clock",
                        ),
                        form_field(
                            "Vía",
                            "Hora de vía",
                            "datetime-local",
                            "via",
                            "clock",
                        ),
                        form_field(
                            "Procedimientos",
                            "Procedimientos",
                            "text",
                            "procedimientos",
                            "clipboard",
                        ),
                        form_field(
                            "Observaciones",
                            "Observaciones",
                            "text",
                            "observaciones",
                            "clipboard-plus",
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Submit Patient"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.add_register_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def update_patient_dialog(patient):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square-pen", size=22),
                rx.text("Edit", size="3"),
                color_scheme="blue",
                size="2",
                variant="solid",
                on_click=lambda: State.get_register(patient),
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Editar paciente",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Editar información del paciente",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Name
                        form_field(
                            "Name", 
                            "Nombre Paciente", 
                            "text", 
                            "nombre", 
                            "paw-print",
                            patient.nombre
                        ),
                        form_field(
                            "Motivo de Hospitalización",
                            "Motivo de Hospitalización",
                            "text",
                            "motivo_hospitalizacion",
                            "clipboard",
                            patient.motivo_hospitalizacion
                        ),
                        form_field(
                            "Médico",
                            "Nombre Médico",
                            "text",
                            "medico_id",
                            "user",
                            patient.medico_id
                        ),
                        form_field(
                            "Técnico",
                            "Nombre Técnico",
                            "text",
                            "tecnico_id",
                            "user",
                            patient.tecnico_id
                        ),
                        form_field_radio(
                            "Estado",
                            "Estado Paciente",
                            "radio",
                            "via",
                            "heart",
                            ["Estable", "Regular", "Critico"]
                        ),
                        form_field_radio(
                            "Prioridad",
                            "Nivel de cuidados",
                            "radio",
                            "via",
                            "shield",
                            ["1.0", "1.5", "2.0"]
                        ),
                        form_field(
                            "Exámenes",
                            "Exámenes paciente",
                            "text",
                            "examenes",
                            "syringe",
                            patient.examenes
                        ),
                        form_field(
                            "Hora de Examen",
                            "Hora de Examen",
                            "datetime-local",
                            "hora_examen",
                            "clock",
                            patient.hora_examen
                        ),
                        form_field(
                            "Ayuno",
                            "Hora Inicio Ayuno",
                            "time",
                            "ayuno",
                            "clock",
                            patient.ayuno
                        ),
                        form_field(
                            "Vía",
                            "Hora de vía",
                            "datetime-local",
                            "via",
                            "clock",
                            patient.via
                        ),
                        form_field(
                            "Procedimientos",
                            "Procedimientos",
                            "text",
                            "procedimientos",
                            "clipboard",
                            patient.procedimientos
                        ),
                        form_field(
                            "Observaciones",
                            "Observaciones",
                            "text",
                            "observaciones",
                            "clipboard-plus",
                            patient.observaciones
                        ),
                    
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Actualizar paciente"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        padding_bottom="1em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.update_register_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def main_table():
    """Main table to display patients."""
    return rx.fragment(
        rx.flex(
            add_patient_button(),
            rx.spacer(),
            rx.checkbox(text="Mostrar pacientes dados de alta", on_change= State.check_alta(),),
            rx.input(
                rx.input.slot(rx.icon("search")),
                placeholder="Search here...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                on_change=lambda value: State.filter_values(value),
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Paciente", "paw-print"),
                    _header_cell("Motivo", "clipboard"),
                    _header_cell("Medico", "user"),
                    _header_cell("Técnico", "user"),
                    _header_cell("Estado", "heart"),  # Nuevo estado del paciente
                    _header_cell("Nivel de Cuidados", "shield"),  # Nuevo nivel de cuidados
                    _header_cell("Exámenes", "syringe"),
                    _header_cell("Hora Examen", "clock"),
                    _header_cell("Ayuno", "clock"),
                    _header_cell("Vía", "clock"),
                    _header_cell("Procedimientos", "clipboard"),
                    _header_cell("Observaciones", "clipboard-plus"),
                    _header_cell("Acciones", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(State.patients, show_patient)),
            variant="surface",
            size="3",
            width="100%",
            on_mount=State.load_entries,
        ),
    )