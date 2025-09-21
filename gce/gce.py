import reflex as rx
from gce.pages.admin import vista_administrador
from gce.pages.student import vista_estudiante
from gce.pages.login import login_page
from gce.pages.register import vista_registro
from .database import create_db_and_tables, init_db

# Create and initialize the database
create_db_and_tables()
init_db()

app = rx.App(
    theme=rx.theme(accent_color="mint", radius="full"),
)
app.add_page(vista_administrador, route="/admin")
app.add_page(vista_estudiante, route="/estudiante")
app.add_page(login_page, route="/login")
app.add_page(vista_registro, route="/register")
app.add_page(login_page, route="/")
