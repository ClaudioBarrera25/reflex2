import reflex as rx
from typing import List



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

datetime_style = {
    "color": "green",
    "font_family": "Arial",
    "border_radius": "5px",
    "border": "2px solid #EE756A",
    "padding": "5px",
}


def form_field_date(
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
            name=name,
            step="300"
            # style=datetime_style
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
            # on_change=lambda value: state_class.set_radio_value,  # Actualizar el estado al cambiar
            # color_scheme=rx.cond(
            #     state_class.radio_value == options[2], "tomato",
            #     rx.cond(
            #         state_class.radio_value == options[1], 
            #         "amber", 
            #         "green")
            # ),
        ),
        direction="column",
        spacing="1",
        width="100%"
    )


