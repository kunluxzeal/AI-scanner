import reflex as rx

from intelliscan.components.cards.stat_card import stat_card
from intelliscan.components.cards.camera_card import camera_card
from intelliscan.components.widgets.activity_feed import activity_feed


def dashboard_page() -> rx.Component:
    return rx.vstack(
        # Dashboard header
        rx.hstack(
            rx.vstack(
                rx.text(
                    "INTELLISCAN / OVERVIEW",
                    size="2",
                    weight="medium",
                    color="var(--accent-11)",
                    letter_spacing="0.12em",
                ),
                rx.heading(
                    "Edge AI Operations",
                    size="8",
                    weight="bold",
                ),
                rx.text(
                    "Monitor your edge intelligence infrastructure.",
                    size="3",
                    color="var(--gray-10)",
                ),
                spacing="1",
                align="start",
            ),

            rx.spacer(),

            rx.hstack(
                rx.box(
                    width="8px",
                    height="8px",
                    border_radius="50%",
                    background="var(--green-9)",
                    box_shadow="0 0 10px var(--green-9)",
                ),
                rx.vstack(
                    rx.text(
                        "SYSTEM ONLINE",
                        size="2",
                        weight="bold",
                        color="var(--green-11)",
                    ),
                    rx.text(
                        "Edge runtime active",
                        size="1",
                        color="var(--gray-10)",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="2",
                align="center",
            ),
            
            width="100%",
            align="center",
        ),

        # KPI cards
        rx.grid(
            stat_card(
                "AI ENGINE",
                "READY",
                "Florence-2",
            ),
            stat_card(
                "CAMERA",
                "OFFLINE",
                "Pi Camera",
            ),
            stat_card(
                "DEVICES",
                "3",
                "Connected devices",
            ),
            stat_card(
                "ANALYSES",
                "128",
                "This session",
            ),
            columns=rx.breakpoints(
                initial="1",
                sm="2",
                lg="4",
            ),
            spacing="4",
            width="100%",
        ),

        # Main workspace
        rx.grid(
            camera_card(),
            activity_feed(),
            columns=rx.breakpoints(
                initial="1",
                lg="2",
            ),
            spacing="4",
            width="100%",
        ),

        spacing="7",
        align="stretch",
        padding="2em",
        width="100%",
    )