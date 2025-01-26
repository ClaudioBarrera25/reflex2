import reflex as rx
from reflex2.components.buttons import button_gatos, button_perros


def land_bienvenida() -> rx.Component:
    return rx.flex(
            rx.text(
                "Bienvenido a la App de Hospital!", 
                size="9",
                align="center",
                weight="bold"
                ),
            rx.flex(
                button_gatos(),
                button_perros(),
                direction = rx.breakpoints(
                    initial="column",
                    md = "row"
                )
            )            ,
            spacing="5",
            justify="center",
            align="center",
            min_height="100vh", # vh es el viewport height que es el tamaño de la ventana de la aplicación.
            width="100%",
            direction="column"
    )
