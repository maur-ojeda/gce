# pages/admin.py
import reflex as rx
from ..components import PageShell, TarjetaCurso, FormularioCurso, admin_only
from ..state import AdminState
from ..components.forms import FormularioCurso

@admin_only
def vista_administrador():
    return PageShell(
        rx.heading("Panel de Administración", size="8", color="white"),
        rx.hstack(
            rx.heading("Cursos", size="6"),
            rx.spacer(),
            rx.button("Crear Curso", on_click=AdminState.toggle_modal, color_scheme="green"),
            width="100%", mt="4"
        ),
        rx.divider(),
        rx.table.root(
        rx.table.header("Cursos Existentes"),
        rx.table.body(
            rx.foreach(
            AdminState.cursos_con_profesores,
                lambda c: rx.table.row(
                    rx.table.cell(c["id"]),
                    rx.table.cell(c["nombre"]),
                    rx.table.cell(c["profesor_nombre"]),
                    rx.table.cell(c["aplicable"]),
                    rx.table.cell(c["horario"]),
                    rx.table.cell(f"{c['cupos_totales']}"),
                    rx.table.cell(f"{c['inscritos_count']}"),
                    rx.table.cell(
                        rx.hstack(
                            rx.button("✏️", size="2",
                            on_click=lambda: AdminState.editar(c["id"])),
                            rx.button("🗑️", size="2", color_scheme="red",
                            on_click=lambda: AdminState.eliminar(c["id"])),
                            spacing="1"
                        )
                    ),
                )
            )
        ),
        width="100%", mt="4"
        ),
        # modal
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Crear / Editar Curso"),
                FormularioCurso(),
                rx.dialog.close(rx.button("Cancelar", variant="soft"))
            ),
            open=AdminState.show_form_modal,
            on_open_change=AdminState.toggle_modal
        ),
    )