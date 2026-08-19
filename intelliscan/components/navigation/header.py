import reflex as rx


def header() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.heading(
                "Dashboard",
                size="6",
            ),
            rx.text(
                "Edge intelligence overview",
                size="2",
            ),
            spacing="1",
            align="start",
        ),

        rx.spacer(),

        rx.hstack(
            rx.text(
                "System Online",
                size="2",
            ),
            rx.color_mode.button(),
            spacing="3",
        ),

        width="100%",
        padding="1.5em 2em",
        border_bottom="1px solid var(--gray-a5)",
    )