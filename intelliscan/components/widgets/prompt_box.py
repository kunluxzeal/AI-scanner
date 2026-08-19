import reflex as rx

from intelliscan.state.vision_state import VisionState


def prompt_box() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    "VISION ANALYSIS",
                    size="1",
                    weight="bold",
                    color="var(--accent-11)",
                    letter_spacing="0.12em",
                ),
                rx.text(
                    "Object Detection",
                    size="3",
                    weight="medium",
                ),
                rx.text(
                    "Gemma will identify objects in the selected image.",
                    size="2",
                    color="var(--gray-9)",
                ),
                spacing="1",
                align="start",
            ),

            rx.spacer(),

            rx.button(
                rx.cond(
                    VisionState.analyzing,
                    rx.spinner(),
                    rx.icon("scan-search"),
                ),
                rx.cond(
                    VisionState.analyzing,
                    "Analyzing...",
                    "Analyze",
                ),
                size="3",
                color_scheme="cyan",
                variant="solid",
                on_click=VisionState.analyze,
                disabled=VisionState.analyzing,
            ),

            width="100%",
            align="center",
        ),

        padding="1.5em",
        background="linear-gradient(145deg, var(--gray-2), var(--accent-a2))",
        border="1px solid var(--accent-a5)",
        border_radius="large",
        width="100%",
    )