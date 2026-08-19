import reflex as rx

from intelliscan.state.vision_state import VisionState


def vision_input() -> rx.Component:
    return rx.box(
        rx.vstack(
          
         rx.hstack(
            rx.vstack(
                rx.text(
                    "IMAGE INPUT",
                    size="1",
                    weight="bold",
                    color="var(--accent-11)",
                    letter_spacing="0.12em",
                ),
                rx.heading(
                    "Vision Capture",
                    size="4",
                    weight="bold",
                ),
                rx.text(
                    "Upload an image for AI analysis.",
                    size="2",
                    color="var(--gray-10)",
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.cond(
                VisionState.image_filename != "",
                rx.badge(
                    "IMAGE READY",
                    color_scheme="cyan",
                ),
                rx.badge(
                    "NO IMAGE",
                    color_scheme="gray",
                ),
            ),
            width="100%",
            align="start",
            ),

                rx.cond(
                VisionState.image_filename != "",
                rx.box(
                    rx.image(
                        src=rx.get_upload_url(
                            VisionState.image_filename
                        ),
                        alt="Uploaded crop image",
                        width="100%",
                        height="350px",
                        object_fit="contain",
                        border_radius="medium",
                    ),
                    width="100%",
                    height="350px",
                    background="var(--gray-2)",
                    border="1px solid var(--gray-a5)",
                    border_radius="large",
                    overflow="hidden",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon(
                            "image",
                            size=48,
                            color="var(--accent-9)",
                        ),
                        rx.text(
                            "No image selected",
                            size="4",
                            weight="medium",
                        ),
                        rx.text(
                            "Upload an image to begin vision analysis.",
                            size="2",
                            color="var(--gray-9)",
                            text_align="center",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    height="350px",
                    width="100%",
                    background=(
                        "linear-gradient("
                        "145deg, "
                        "var(--gray-2), "
                        "var(--gray-3)"
                        ")"
                    ),
                    border="1px dashed var(--gray-a6)",
                    border_radius="large",
                ),
            ),

            rx.hstack(
                rx.upload(
                    rx.button(
                        rx.icon("upload"),
                        "Upload Image",
                        variant="outline",
                        size="3",
                    ),
                    id="vision_upload",
                    accept={
                        "image/png": [".png"],
                        "image/jpeg": [".jpg", ".jpeg"],
                        "image/webp": [".webp"],
                    },
                    max_files=1,
                    on_drop=VisionState.handle_upload(
                        rx.upload_files(
                            upload_id="vision_upload"
                        )
                    ),
                    border="none",
                    padding="0",
                ),

                rx.button(
                    rx.icon("scan"),
                    rx.cond(
                        VisionState.analyzing,
                        "Analyzing...",
                        "Analyze",
                    ),
                    size="3",
                    loading=VisionState.analyzing,
                    disabled=(
                        (VisionState.image_path == "")
                        | VisionState.analyzing
                    ),
                    on_click=VisionState.analyze,
                ),

                

                spacing="3",
            ),

            rx.hstack(
                rx.icon(
                    "circle_check",
                    size=16,
                    color="var(--accent-9)",
                ),
                rx.text(
                    VisionState.status,
                    size="2",
                    color="var(--gray-10)",
                ),
                spacing="2",
            ),

            rx.cond(
                VisionState.error_message != "",
                rx.callout(
                    VisionState.error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    width="100%",
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