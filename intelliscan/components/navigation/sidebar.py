import reflex as rx


def nav_item(label: str, href: str) -> rx.Component:
    active = rx.State.router.page.path == href

    return rx.link(
        rx.button(
            label,
            width="100%",
            variant=rx.cond(active, "soft", "ghost"),
            color_scheme=rx.cond(active, "cyan", "gray"),
            justify_content="flex-start",
        ),
        href=href,
        width="100%",
        underline="none",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                "IntelliScan",
                size="6",
            ),

            rx.text(
                "EDGE AI PLATFORM",
                size="1",
                weight="bold",
            ),

            rx.divider(),

            rx.vstack(
                nav_item("Dashboard", "/"),
                nav_item("Vision", "/vision"),
                nav_item("Devices", "/devices"),
                nav_item("History", "/history"),
                nav_item("Settings", "/settings"),
                width="100%",
                spacing="2",
            ),

            rx.spacer(),

            rx.box(
                rx.text(
                    "SYSTEM STATUS",
                    size="1",
                    weight="bold",
                ),
                rx.text(
                    "● Online",
                    size="2",
                ),
                width="100%",
                padding="1em",
                border_radius="medium",
            ),

            width="100%",
            height="100%",
            spacing="5",
            align="stretch",
        ),
        width="250px",
        height="100vh",
        padding="1.5em",
        border_right="1px solid var(--gray-a5)",
    )