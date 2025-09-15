import reflex as rx
from ..state import State
# from ..models import Curso

# --- Vista de Estudiante ---

def tarjeta_curso(curso: dict, mostrar_boton_inscribir: bool = False):
    """Componente reutilizable para mostrar un curso."""
    return rx.card(
        rx.flex(
            rx.heading(curso["nombre"], size="4"),
            rx.text(f"Profesor: {curso['profesor_nombre']}", size="2", color="gray"),
            rx.text(f"Horario: {curso['horario']}", size="2"),
            rx.text(f"Cupos: {curso['cupos_disponibles']}/{curso['cupos_totales']}", size="2"),
            rx.text(curso["descripcion"], size="2", margin_top="1"),
            rx.hstack(
                rx.button(
                    "Ver detalles",
                    size="2",
                    variant="outline",
                    on_click=lambda: State.mostrar_detalle_curso(curso["id"])
                ),
                rx.cond(
                    mostrar_boton_inscribir,
                    rx.button(
                        "Inscribirme",
                        size="2",
                        color_scheme="green",
                        on_click=lambda: State.inscribir_curso(curso["id"])
                    )
                ),
                spacing="2",
                margin_top="2"
            ),
            direction="column",
            spacing="2"
        ),
        width="100%"
    )

def vista_estudiante():
    """Vista principal para estudiantes."""
    return rx.vstack(
        rx.cond(
            State.rol_actual != "estudiante",
            rx.redirect("/"),
            rx.console_log('Estudiante') 
        ),
        
        rx.heading(
            rx.cond(                
                State.estudiante_actual.nombre != "",
                f"Bienvenido, {State.estudiante_actual.nombre}",
                "Bienvenido, Estudiante"
            ),
            size="8"
        ),
        
        # Mensajes
        rx.cond(
            State.mensaje_exito != "",
            rx.callout(
                State.mensaje_exito,
                icon="check",
                color_scheme="green",
                role="alert"
            )
        ),
        rx.cond(
            State.mensaje_error != "",
            rx.callout(
                State.mensaje_error,
                icon="triangle_alert",
                color_scheme="red",
                role="alert"
            )
        ),
        
        # Cursos inscritos
        rx.vstack(
            rx.heading("Mis Cursos", size="6"),
            rx.cond(
                State.cursos_inscritos.length() == 0,
                rx.text("No estás inscrito en ningún curso aún.", color="gray"),
                rx.foreach(
                    State.cursos_inscritos,
                    lambda curso: tarjeta_curso(curso)
                )
            ),
            width="100%",
            spacing="4"
        ),
        
        # Cursos disponibles
        rx.vstack(
            rx.heading("Cursos Disponibles", size="6"),
            rx.cond(
                State.cursos_disponibles.length() == 0,
                rx.text("No hay cursos disponibles en este momento.", color="gray"),
                rx.foreach(
                    State.cursos_disponibles,
                    lambda curso: tarjeta_curso(curso, mostrar_boton_inscribir=True)
                )
            ),
            width="100%",
            spacing="4"
        ),
        
        # Modal de detalles
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Detalles del Curso"),
                rx.cond(
                    State.curso_detalle_id != -1,
                    rx.vstack(
                        rx.foreach(
                            State.cursos_con_profesores,
                            lambda curso: rx.cond(
                                curso["id"] == State.curso_detalle_id,
                                rx.vstack(
                                    rx.heading(curso["nombre"], size="6"),
                                    rx.text(f"Profesor: {curso['profesor_nombre']}"),
                                    rx.text(f"Descripción: {curso['descripcion']}"),
                                    rx.text(f"Aplicable para: {curso['aplicable']}"),
                                    rx.text(f"Horario: {curso['horario']}"),
                                    rx.text(f"Cupos: {curso['cupos_disponibles']}/{curso['cupos_totales']}"),
                                    rx.hstack(
                                        rx.button(
                                            "Inscribirme",
                                            color_scheme="green",
                                            on_click=lambda: State.inscribir_curso(curso["id"])
                                        ),
                                        rx.button(
                                            "Cerrar",
                                            on_click=State.toggle_detalle_modal
                                        ),
                                        spacing="3",
                                        margin_top="4"
                                    ),
                                    width="100%"
                                )
                            )
                        )
                    )
                ),
                rx.cond(
                    State.mensaje_error != "",
                    rx.callout(
                        State.mensaje_error,
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                        margin_top="3"
                    )
                ),
                rx.cond(
                    State.mensaje_exito != "",
                    rx.callout(
                        State.mensaje_exito,
                        icon="check",
                        color_scheme="green",
                        role="alert",
                        margin_top="3"
                    )
                )
            ),
            open=State.show_detalle_modal,
            on_open_change=State.toggle_detalle_modal
        ),
        
        width="100%",
        max_width="800px",
        padding="20px",
        spacing="6"
    )