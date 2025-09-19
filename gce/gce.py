import reflex as rx
from gce.pages.admin import vista_administrador
from gce.pages.student import vista_estudiante
from gce.pages.login import login_page

app = rx.App(
    theme=rx.theme(accent_color="mint", radius="full"),
)
app.add_page(vista_administrador, route="/admin")
app.add_page(vista_estudiante, route="/estudiante")
app.add_page(login_page, route="/login")
app.add_page(login_page, route="/")