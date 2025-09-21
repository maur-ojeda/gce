import reflex as rx
from ..components import PageShell
from ..state.register import RegisterState

def vista_registro():
    return PageShell(
        rx.heading("Registro de Usuario", size="8", color="white"),
        rx.vstack(
            rx.input(placeholder="Nombre Completo", on_blur=RegisterState.set_nombre, mb=4),
            rx.input(placeholder="Correo Electrónico", on_blur=RegisterState.set_email, mb=4),
            rx.input(placeholder="Contraseña", on_blur=RegisterState.set_password, type="password", mb=4),
            rx.button("Registrarse", on_click=RegisterState.handle_registration, width="100%"),
            rx.cond(
                RegisterState.mensaje != "",
                rx.callout(RegisterState.mensaje, color="green", mt=4)
            ),
            width="100%",
            spacing="4",
            max_width="400px",
            margin="auto",
            padding="20px",
            border_radius="10px",
            bg="#f0f0f0",
        ),
    )
