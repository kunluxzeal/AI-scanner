import reflex as rx


def stat_card(
    title: str,
    value: str,
    description: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    title,
                    size="2",
                    weight="medium",
                    color="var(--gray-11)",
                    letter_spacing="0.08em",
                ),

                rx.spacer(),

                rx.box(
                    width="8px",
                    height="8px",
                    border_radius="50%",
                    background="var(--accent-9)",
                    box_shadow="0 0 10px var(--accent-9)",
                ),

                width="100%",
            ),

            rx.heading(
                value,
                size="7",
                weight="bold",
                color="var(--accent-11)",
            ),

            rx.text(
                description,
                size="2",
                color="var(--gray-10)",
            ),

            spacing="2",
            align="start",
            width="100%",
        ),

        padding="1.5em",
        background="linear-gradient(145deg, var(--gray-2), var(--gray-3))",
        border="1px solid var(--gray-a5)",
        border_radius="large",
        width="100%",
        min_height="150px",

        box_shadow="0 4px 20px var(--gray-a3)",

        transition="all 150ms ease",

        _hover={
            "border_color": "var(--accent-7)",
            "transform": "translateY(-3px)",
            "box_shadow": "0 10px 30px var(--gray-a4)",
        },
    )