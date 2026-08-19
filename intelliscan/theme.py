import reflex as rx


def app_theme():
    return rx.theme(
        appearance="dark",
        accent_color="cyan",
        gray_color="slate",
        radius="medium",
        scaling="100%",
        has_background=True,
    )