import reflex as rx


def form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    default_value: str = "",
) -> rx.Component:
    return rx.flex(
        rx.hstack(
            rx.icon(icon, size=16, stroke_width=1.5),
            rx.text(label),
            align="center",
            spacing="2",
        ),
        rx.input(
            placeholder=placeholder,
            type=type,
            default_value=default_value,
            name=name
        ),
        direction="column",
        spacing="1",
        width="100%"
    )

def form_field_radio(
    label: str,
    placeholder: str,
    type: str, 
    name: str,
    icon: str,
    options: list = [],
    default_value: str = "",
    state_class: type[rx.State] = None,
) -> rx.Component:
    return rx.flex(
        rx.hstack(
            rx.icon(icon, size=16, stroke_width=1.5),
            rx.text(label),
            align="center",
            spacing="2",
        ),
        rx.radio_group(
            options,         
            default_value= rx.cond(default_value=="", options[0], default_value), # Si el valor default esta vacio, entregar la primera opcion.
            direction="row",
            name=name,
            on_change=lambda value: state_class.set_radio_value,  # Actualizar el estado al cambiar
            color_scheme=rx.cond(
                state_class.radio_value == options[2], "red",
                rx.cond(
                    state_class.radio_value == options[1], 
                    "yellow", 
                    "green")
            ),
        ),
        direction="column",
        spacing="1",
        width="100%"
    )