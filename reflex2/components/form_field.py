import reflex as rx


def form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    default_value: str = "",
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.icon(icon, size=16, stroke_width=1.5),
                rx.form.label(label),
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(placeholder=placeholder, type=type, default_value=default_value ),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )


def form_field_radio(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    options: list = [],
    default_value: str = "",
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.icon(icon, size=16, stroke_width=1.5),
                rx.form.label(label),
                align="center",
                spacing="2",
            ),
            rx.radio_group(
                options,
                default_value=options[0],
                direction="row",
                name=name,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%"
    )