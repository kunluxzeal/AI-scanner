import reflex as rx


def activity_item(
    title: str,
    description: str,
    time: str,
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                width="8px",
                height="8px",
                border_radius="50%",
                background="var(--accent-9)",
                box_shadow="0 0 8px var(--accent-9)",
                margin_top="5px",
                flex_shrink="0",
            ),

            rx.vstack(
                rx.hstack(
                    rx.text(
                        title,
                        size="2",
                        weight="medium",
                        color="var(--gray-12)",
                    ),
                    rx.spacer(),
                    rx.text(
                        time,
                        size="1",
                        color="var(--gray-9)",
                    ),
                    width="100%",
                ),

                rx.text(
                    description,
                    size="1",
                    color="var(--gray-10)",
                ),

                spacing="1",
                align="start",
                width="100%",
            ),

            spacing="3",
            align="start",
            width="100%",
        ),

        padding="0.75em",
        border_radius="medium",
        width="100%",
        transition="all 150ms ease",

        _hover={
            "background": "var(--gray-a3)",
        },
    )


def activity_feed() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "ACTIVITY LOG",
                        size="1",
                        weight="medium",
                        color="var(--accent-11)",
                        letter_spacing="0.12em",
                    ),
                    rx.heading(
                        "Recent Activity",
                        size="4",
                        weight="bold",
                    ),
                    spacing="0",
                    align="start",
                ),

                rx.spacer(),

                rx.hstack(
                    rx.box(
                        width="7px",
                        height="7px",
                        border_radius="50%",
                        background="var(--green-9)",
                        box_shadow="0 0 8px var(--green-9)",
                    ),
                    rx.text(
                        "LIVE",
                        size="1",
                        weight="bold",
                        color="var(--green-11)",
                    ),
                    spacing="2",
                    align="center",
                ),

                width="100%",
                align="center",
            ),

            rx.divider(),

            activity_item(
                "System started",
                "IntelliScan is ready.",
                "11:42",
            ),

            activity_item(
                "Camera initialized",
                "Waiting for camera stream.",
                "11:41",
            ),

            activity_item(
                "AI engine ready",
                "AI is ready for analysis.",
                "11:40",
            ),

            activity_item(
                "Dashboard loaded",
                "Interface initialized successfully.",
                "11:39",
            ),

            spacing="3",
            align="stretch",
            width="100%",
        ),

        padding="1.5em",
        background="linear-gradient(145deg, var(--gray-2), var(--gray-3))",
        border="1px solid var(--gray-a5)",
        border_radius="large",
        width="100%",
        min_height="300px",
        box_shadow="0 4px 20px var(--gray-a3)",
    )