import reflex as rx


def devices_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Devices", size="8"),
        rx.text(
            "Monitor connected edge devices and sensors.",
            size="4",
        ),
        spacing="3",
        align="start",
        padding="2em",
        width="100%",
    )