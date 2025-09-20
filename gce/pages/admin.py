# pages/admin.py
import reflex as rx
from ..components import PageShell, FormularioCurso
from ..state.admin import AdminState
from ..state.base import BaseState

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
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Profesor Principal"),
                rx.table.column_header_cell("Profesor Suplente"), # Add this
                rx.table.column_header_cell("Aplicable"),
                rx.table.column_header_cell("Horario"),
                rx.table.column_header_cell("Cupos Totales"),
                rx.table.column_header_cell("Inscritos"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(
            AdminState.cursos_con_profesores,
                lambda c: rx.table.row(
                    rx.table.cell(c["id"]),
                    rx.table.cell(c["nombre"]),
                    rx.table.cell(c["profesor_nombre"]),
                    rx.table.cell(c["profesor_suplente_nombre"]),
                    rx.table.cell(c["aplicable"]),
                    rx.table.cell(c["horario"]),
                    rx.table.cell(f"{c['cupos_totales']}"),
                    rx.table.cell(f"{c['inscritos_count']}"),
                    rx.table.cell(
                        rx.hstack(
                            rx.button("✏️", size="2",
                            on_click=lambda: AdminState.editar(c["id"])),
                            rx.button("🗑️", size="2", color_scheme="red",
                            on_click=lambda: AdminState.preparar_eliminacion(c["id"])),
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
                FormularioCurso(profesor_nombres=AdminState.profesor_nombres),
                rx.dialog.close(rx.button("Cancelar", variant="soft"))
            ),
            open=AdminState.show_form_modal,
            on_open_change=AdminState.toggle_modal
        ),
        # Delete Confirmation Dialog
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.alert_dialog.title("Confirmar Eliminación"),
                rx.alert_dialog.description(
                    "¿Estás seguro de que quieres eliminar este curso? Esta acción no se puede deshacer."
                ),
                rx.flex(
                    rx.alert_dialog.cancel(
                        rx.button("Cancelar", variant="soft", color_scheme="gray")
                    ),
                    rx.alert_dialog.action(
                        rx.button(
                            "Eliminar",
                            color_scheme="red",
                            on_click=AdminState.eliminar,
                        )
                    ),
                    spacing="3",
                    margin_top="15px",
                    justify="end",
                ),
            ),
            open=AdminState.show_delete_dialog,
            on_open_change=AdminState.cancelar_eliminacion,
        ),
    )

vista_administrador.on_load = BaseState.require_admin