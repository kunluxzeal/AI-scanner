import reflex as rx

from intelliscan.state.vision_state import VisionState


def analysis_panel() -> rx.Component:
    return rx.box(
        rx.vstack(

            # ============================================================
            # HEADER
            # ============================================================

            rx.hstack(
                rx.vstack(
                    rx.text(
                        "AI ENGINE",
                        size="1",
                        weight="bold",
                        color="var(--accent-11)",
                        letter_spacing="0.12em",
                    ),
                    rx.heading(
                        "AI Analysis",
                        size="4",
                        weight="bold",
                    ),
                    rx.text(
                        "Gemma 4 E2B",
                        size="2",
                        color="var(--gray-10)",
                    ),
                    spacing="1",
                    align="start",
                ),

                rx.spacer(),

                rx.cond(
                    VisionState.analyzing,
                    rx.badge(
                        "ANALYZING",
                        color_scheme="cyan",
                    ),
                    rx.cond(
                        VisionState.condition != "",
                        rx.badge(
                            "COMPLETE",
                            color_scheme="green",
                        ),
                        rx.badge(
                            "READY",
                            color_scheme="gray",
                        ),
                    ),
                ),

                width="100%",
                align="start",
            ),

            # ============================================================
            # CONTENT
            # ============================================================

            rx.cond(
                VisionState.condition != "",

                # ========================================================
                # ANALYSIS RESULTS
                # ========================================================

                rx.vstack(

                    # Condition
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "CROP CONDITION",
                                    size="1",
                                    weight="bold",
                                    color="var(--gray-9)",
                                    letter_spacing="0.1em",
                                ),
                                rx.heading(
                                    VisionState.condition,
                                    size="7",
                                    color=rx.cond(
                                        VisionState.condition == "GOOD",
                                        "var(--green-11)",
                                        "var(--red-11)",
                                    ),
                                ),
                                spacing="1",
                                align="start",
                            ),

                            rx.spacer(),

                            rx.badge(
                                VisionState.crop,
                                color_scheme="cyan",
                                size="3",
                            ),

                            width="100%",
                            align="center",
                        ),
                        padding="1.25em",
                        background=rx.cond(
                            VisionState.condition == "GOOD",
                            "var(--green-a2)",
                            "var(--red-a2)",
                        ),
                        border=rx.cond(
                            VisionState.condition == "GOOD",
                            "1px solid var(--green-a5)",
                            "1px solid var(--red-a5)",
                        ),
                        border_radius="large",
                        width="100%",
                    ),

                    # External inspection
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "EXTERNAL INSPECTION",
                                size="1",
                                weight="bold",
                                color="var(--gray-9)",
                                letter_spacing="0.1em",
                            ),
                            rx.text(
                                VisionState.external,
                                size="3",
                                line_height="1.5",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        padding="1.25em",
                        background="var(--gray-a2)",
                        border="1px solid var(--gray-a4)",
                        border_radius="medium",
                        width="100%",
                    ),

                    # Internal inspection
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "INTERNAL INSPECTION",
                                size="1",
                                weight="bold",
                                color="var(--gray-9)",
                                letter_spacing="0.1em",
                            ),
                            rx.text(
                                VisionState.internal,
                                size="3",
                                line_height="1.5",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        padding="1.25em",
                        background="var(--gray-a2)",
                        border="1px solid var(--gray-a4)",
                        border_radius="medium",
                        width="100%",
                    ),

                    # Defect
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "DEFECT",
                                size="1",
                                weight="bold",
                                color="var(--gray-9)",
                                letter_spacing="0.1em",
                            ),
                            rx.text(
                                VisionState.defect,
                                size="3",
                                line_height="1.5",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        padding="1.25em",
                        background=rx.cond(
                            VisionState.condition == "DEFECTIVE",
                            "var(--red-a2)",
                            "var(--gray-a2)",
                        ),
                        border=rx.cond(
                            VisionState.condition == "DEFECTIVE",
                            "1px solid var(--red-a5)",
                            "1px solid var(--gray-a4)",
                        ),
                        border_radius="medium",
                        width="100%",
                    ),

                    # Metadata
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "INFERENCE",
                                    size="1",
                                    color="var(--gray-9)",
                                ),
                                rx.text(
                                    VisionState.inference_time.to_string()
                                    + " s",
                                    size="3",
                                    weight="bold",
                                ),
                                spacing="1",
                                align="start",
                            ),
                            padding="1em",
                            background="var(--gray-a2)",
                            border="1px solid var(--gray-a4)",
                            border_radius="medium",
                        ),

                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "DEVICE",
                                    size="1",
                                    color="var(--gray-9)",
                                ),
                                rx.text(
                                    VisionState.device,
                                    size="3",
                                    weight="bold",
                                ),
                                spacing="1",
                                align="start",
                            ),
                            padding="1em",
                            background="var(--gray-a2)",
                            border="1px solid var(--gray-a4)",
                            border_radius="medium",
                        ),

                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "IMAGE",
                                    size="1",
                                    color="var(--gray-9)",
                                ),
                                rx.text(
                                    VisionState.image_width.to_string()
                                    + " × "
                                    + VisionState.image_height.to_string(),
                                    size="3",
                                    weight="bold",
                                ),
                                spacing="1",
                                align="start",
                            ),
                            padding="1em",
                            background="var(--gray-a2)",
                            border="1px solid var(--gray-a4)",
                            border_radius="medium",
                        ),

                        columns="3",
                        spacing="3",
                        width="100%",
                    ),

                    # Model
                    rx.box(
                        rx.hstack(
                            rx.text(
                                "MODEL",
                                size="1",
                                weight="bold",
                                color="var(--gray-9)",
                            ),
                            rx.spacer(),
                            rx.badge(
                                VisionState.model,
                                color_scheme="cyan",
                            ),
                            width="100%",
                            align="center",
                        ),
                        padding="1em",
                        background="var(--gray-a2)",
                        border="1px solid var(--gray-a4)",
                        border_radius="medium",
                        width="100%",
                    ),

                    spacing="4",
                    align="stretch",
                    width="100%",
                ),

                # ========================================================
                # NO RESULTS YET
                # ========================================================

                rx.center(
                    rx.cond(
                        VisionState.analyzing,

                        # ==================================================
                        # ANALYZING
                        # ==================================================

                        rx.vstack(
                            rx.icon(
                                "scan",
                                size=42,
                                color="var(--accent-9)",
                                class_name="analysis-pulse",
                            ),

                            rx.text(
                                "Analyzing image",
                                size="3",
                                weight="medium",
                            ),

                            rx.text(
                                "Gemma 4 E2B is inspecting the image...",
                                size="2",
                                color="var(--gray-9)",
                                text_align="center",
                            ),

                            rx.hstack(
                                rx.text(
                                    "Processing",
                                    size="2",
                                    color="var(--gray-9)",
                                ),

                                rx.text(
                                    "●",
                                    size="2",
                                    color="var(--accent-9)",
                                    class_name="dot-1",
                                ),

                                rx.text(
                                    "●",
                                    size="2",
                                    color="var(--accent-9)",
                                    class_name="dot-2",
                                ),

                                rx.text(
                                    "●",
                                    size="2",
                                    color="var(--accent-9)",
                                    class_name="dot-3",
                                ),

                                spacing="1",
                            ),

                            spacing="3",
                            align="center",
                        ),

                        # ==================================================
                        # WAITING
                        # ==================================================

                        rx.vstack(
                            rx.icon(
                                "sparkles",
                                size=48,
                                color="var(--accent-9)",
                            ),

                            rx.text(
                                "Waiting for image analysis",
                                size="3",
                                weight="medium",
                            ),

                            rx.text(
                                "Upload an image and select Analyze.",
                                size="2",
                                color="var(--gray-9)",
                                text_align="center",
                            ),

                            spacing="3",
                            align="center",
                        ),
                    ),

                    min_height="350px",
                    width="100%",
                    background=(
                        "radial-gradient("
                        "circle at center, "
                        "var(--accent-a2), "
                        "var(--gray-a2) 55%, "
                        "var(--gray-a3)"
                        ")"
                    ),
                    border="1px solid var(--gray-a5)",
                    border_radius="large",
                ),
            ),

            spacing="5",
            align="stretch",
            width="100%",
        ),

        padding="1.5em",
        background=(
            "linear-gradient("
            "145deg, "
            "var(--gray-2), "
            "var(--gray-3)"
            ")"
        ),
        border="1px solid var(--gray-a5)",
        border_radius="large",
        width="100%",
        box_shadow="0 4px 20px var(--gray-a3)",
    )