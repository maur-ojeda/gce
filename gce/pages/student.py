# pages/student.py
import reflex as rx
from ..components import PageShell, TarjetaCurso
from ..state.student import StudentState
from ..state.base import BaseState

def vista_estudiante():
    return PageShell(
        rx.heading(f"Bienvenido, {StudentState.estudiante_actual.nombre}", size="8", color="white" ),
        rx.cond(
            StudentState.mensaje != "",
            rx.callout(StudentState.mensaje, color="green")
        ),
        rx.vstack(
            rx.heading("Mis Cursos", size="6"),
                rx.foreach(
                    StudentState.cursos_inscritos,
                    lambda c: TarjetaCurso(c)
                    ),
                    width="100%", spacing="4"
        ),
        rx.vstack(
            rx.heading("Cursos Disponibles", size="6"),
            rx.foreach(
                StudentState.cursos_disponibles,
                lambda c: TarjetaCurso(c, mostrar_boton_inscribir=True)
                ),
            width="100%", spacing="4"
        ),
        # modal detalle
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Detalles del curso"),
                rx.foreach(
                        StudentState.cursos_con_profesores,
                        lambda c: rx.cond(c["id"] == StudentState.detalle_curso_id,
                        rx.vstack(
                            rx.heading(c["nombre"], size="6"),
                            rx.text(f"Profesor: {c['profesor_nombre']}"),
                            rx.cond(
                                c["profesor_suplente_nombre"] != "N/A", # Only show if not N/A
                                rx.text(f"Profesor Suplente: {c['profesor_suplente_nombre']}"),
                            ),
                            rx.text(f"Descripción: {c['descripcion']}"),
                            rx.text(f"Aplicable: {c['aplicable']}"),
                            rx.text(f"Horario: {c['horario']}"),
                            rx.text(f"Cupos: {c.get('cupos_disponibles', 0)}/{c['cupos_totales']}"),
                            rx.hstack(
                                rx.button("Inscribirme", color_scheme="green", on_click=lambda: StudentState.inscribir(c["id"])),
                                rx.button("Cerrar", on_click=StudentState.mostrar_detalle(-1)),
                                spacing="3", mt="4"
                            )
                        )
                )
                ),
            ),
            open=StudentState.show_detalle_modal,
            on_open_change=StudentState.mostrar_detalle(-1)
        ),
    )

vista_estudiante.on_load = BaseState.require_student