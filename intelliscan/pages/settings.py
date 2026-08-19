import reflex as rx


def settings_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Settings", size="8"),
        rx.text(
            "Configure IntelliScan.",
            size="4",
        ),
        spacing="3",
        align="start",
        padding="2em",
        width="100%",
    )