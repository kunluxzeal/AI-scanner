import reflex as rx

from intelliscan.components.widgets.analysis_panel import analysis_panel
from intelliscan.components.widgets.prompt_box import prompt_box
from intelliscan.components.widgets.vision_input import vision_input


def vision_page() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.heading(
                "AI Vision",
                size="8",
            ),
            rx.text(
                "Gemma visual intelligence workspace.",
                size="3",
            ),
            spacing="1",
            align="start",
        ),

        rx.grid(
            vision_input(),
            analysis_panel(),
            columns=rx.breakpoints(
                initial="1",
                lg="2",
            ),
            spacing="4",
            width="100%",
        ),

        prompt_box(),

        spacing="6",
        align="stretch",
        padding="2em",
        width="100%",
    )