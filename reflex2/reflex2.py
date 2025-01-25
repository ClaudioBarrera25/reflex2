import reflex as rx
import reflex_chakra as rc
from reflex_calendar import calendar
from .components.stats_cards import stats_cards_group
from .views.navbar import navbar
from .views.table import main_table


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        # stats_cards_group(),
        rx.box(
            main_table(),
            width="100%",
        ),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )


def testeo() -> rx.Component:
    return rx.vstack(
        calendar(
            show_neighbouring_month=True
        ),
        rx.input(
            type="datetime-local",
            min="2025-01-20T08:30",
            step="300"
        ),
        rx.select(
            ["04:00", "04:30", "05:00"],
            value="04:00"
        ),
        rx.box(
            "Hello World",
            class_name="text-4xl text-center text-blue-300",
        )
    )




app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="violet"
    ),
)

app.add_page(
    index,
    title="Hospital App",
    description="Aplicación simple para el manejo de hospital.",
)

app.add_page(
    testeo,
    route="/testeo")