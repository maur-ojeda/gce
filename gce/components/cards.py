# components/cards.py
import reflex as rx
from ..state import StudentState as StudentState


def TarjetaCurso(curso: dict, mostrar_boton_inscribir: bool = False):
    """Tarjeta única para admin y student."""
    return rx.card(
            rx.vstack(
                rx.heading(curso["nombre"], size="4"),
                rx.text(f"Profesor: {curso['profesor_nombre']}", size="2", color="gray"),
                rx.text(f"Horario: {curso['horario']}", size="2"),
                rx.text(f"Cupos: {curso.get('cupos_disponibles', 0)}/{curso['cupos_totales']}", size="2"),
                rx.text(curso["descripcion"], size="2", mt="1"),
                rx.hstack(
                    rx.button("Ver detalles", size="2", variant="outline",
                    on_click=lambda: StudentState.mostrar_detalle(curso["id"])),
                    rx.cond(
                        mostrar_boton_inscribir,
                        rx.button("Inscribirme", size="2", color_scheme="green",
                        on_click=lambda: StudentState.inscribir(curso["id"]))
                    ),
                    spacing="2", mt="2"
                ),
                spacing="2"
            )
    )
