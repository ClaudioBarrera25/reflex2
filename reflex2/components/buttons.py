import reflex as rx 
from reflex2.styles.style import style_button_perros, style_button_perros_hover, style_button_gatos, style_button_gatos_hover

def button_perros():
    return rx.button(
        rx.hstack(rx.icon("dog") ,rx.text("Hospital perro")),
        size="4",
        style=style_button_perros,
        _hover=style_button_perros_hover
    )


def button_gatos():
    return rx.button(
        rx.hstack(rx.icon("cat") ,rx.text("Hospital gato")),
        size="4",
        style=style_button_gatos,
        _hover=style_button_gatos_hover
    )