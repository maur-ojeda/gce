# gce/pages/login.py
import reflex as rx
from gce.state import BaseState

def login_page():
    return rx.center(
        rx.vstack(
            rx.heading("Bienvenido al Gestor de Cursos", size="8"),
            rx.text("Por favor, selecciona tu rol para continuar:"),
            rx.hstack(
                rx.button(
                    "Entrar como Administrador",
                    on_click=lambda: BaseState.login("administrador"),
                    size="3",
                    color_scheme="blue"
                ),
                rx.button(
                    "Entrar como Estudiante",
                    on_click=lambda: BaseState.login("estudiante"),
                    size="3",
                    color_scheme="green"
                ),
                spacing="4",
                margin_top="2rem"
            ),
            align="center",
            spacing="4",
            padding="2rem",
            border_radius="lg",
            box_shadow="lg",
            bg="white"
        ),
        height="100vh"
    )
