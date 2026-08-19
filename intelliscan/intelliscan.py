import reflex as rx

from intelliscan.components.navigation.header import header
from intelliscan.components.navigation.sidebar import sidebar
from intelliscan.pages.dashboard import dashboard_page
from intelliscan.pages.devices import devices_page
from intelliscan.pages.history import history_page
from intelliscan.pages.settings import settings_page
from intelliscan.pages.vision import vision_page
from intelliscan.theme import app_theme

from intelliscan.pages.dashboard import dashboard_page


def app_layout(content: rx.Component) -> rx.Component:
    return rx.hstack(
        sidebar(),

        rx.vstack(
            header(),
            content,
            flex="1",
            height="100vh",
            spacing="0",
            overflow="auto",
        ),

        width="100%",
        height="100vh",
        spacing="0",
    )


app = rx.App(
    theme=app_theme(),
)


app.add_page(
    lambda: app_layout(dashboard_page()),
    route="/",
    title="IntelliScan",
)

app.add_page(
    lambda: app_layout(vision_page()),
    route="/vision",
    title="AI Vision | IntelliScan",
)

app.add_page(
    lambda: app_layout(devices_page()),
    route="/devices",
    title="Devices | IntelliScan",
)

app.add_page(
    lambda: app_layout(history_page()),
    route="/history",
    title="History | IntelliScan",
)

app.add_page(
    lambda: app_layout(settings_page()),
    route="/settings",
    title="Settings | IntelliScan",
)