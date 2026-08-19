import reflex as rx


def history_page() -> rx.Component:
    return rx.vstack(
        rx.heading("History", size="8"),
        rx.text(
            "Review previous AI analyses and system activity.",
            size="4",
        ),
        spacing="3",
        align="start",
        padding="2em",
        width="100%",
    )