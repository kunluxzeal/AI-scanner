import reflex as rx


def camera_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    "Camera Preview",
                    size="4",
                ),
                rx.spacer(),
                rx.badge(
                    "Offline",
                    color_scheme="gray",
                ),
                width="100%",
            ),

            rx.center(
                rx.vstack(
                    rx.icon(
                        "camera",
                        size=48,
                    ),
                    rx.text(
                        "No camera feed",
                        size="3",
                        weight="medium",
                    ),
                    rx.text(
                        "Camera will appear here when connected.",
                        size="2",
                    ),
                    spacing="2",
                    align="center",
                ),
                height="300px",
                width="100%",
                border="1px dashed var(--gray-a6)",
                border_radius="medium",
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        padding="1.5em",
        border="1px solid var(--gray-a5)",
        border_radius="large",
        width="100%",
    )