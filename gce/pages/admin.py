# pages/admin.py
import reflex as rx
from ..components import PageShell, FormularioCurso
from ..state.admin import AdminState
from ..state.base import BaseState

# --- Forms --- #
def student_form():
    return rx.vstack(
        rx.input(value=AdminState.student_nombre, placeholder="Nombre Completo", on_change=AdminState.set_student_nombre, width="100%"),
        rx.input(value=AdminState.student_email, placeholder="Correo Electrónico", on_change=AdminState.set_student_email, width="100%"),
        rx.input(value=AdminState.student_nivel, placeholder="Nivel", on_change=AdminState.set_student_nivel, width="100%"),
        rx.input(placeholder="Contraseña (dejar en blanco para no cambiar)", type="password", on_change=AdminState.set_student_password, width="100%"),
        rx.button("Guardar", on_click=AdminState.save_student, width="100%"),
        spacing="4", width="100%"
    )

def teacher_form():
    return rx.vstack(
        rx.input(value=AdminState.teacher_nombre, placeholder="Nombre Completo", on_change=AdminState.set_teacher_nombre, width="100%"),
        rx.input(value=AdminState.teacher_email, placeholder="Correo Electrónico", on_change=AdminState.set_teacher_email, width="100%"),
        rx.input(placeholder="Contraseña (dejar en blanco para no cambiar)", type="password", on_change=AdminState.set_teacher_password, width="100%"),
        rx.heading("Asignar Cursos (Principal)", size="4", margin_top="1em"),
        rx.vstack(
            rx.foreach(AdminState.cursos, lambda curso:
                rx.checkbox(
                    curso.nombre,
                    checked=AdminState.teacher_courses_primary.contains(curso.id),
                    on_change=lambda is_checked: AdminState.toggle_teacher_course_primary(curso.id)
                )
            ),
            align_items="start"
        ),
        rx.heading("Asignar Cursos (Suplente)", size="4", margin_top="1em"),
        rx.vstack(
            rx.foreach(AdminState.cursos, lambda curso:
                rx.checkbox(
                    curso.nombre,
                    checked=AdminState.teacher_courses_substitute.contains(curso.id),
                    on_change=lambda is_checked: AdminState.toggle_teacher_course_substitute(curso.id)
                )
            ),
            align_items="start"
        ),
        rx.button("Guardar", on_click=AdminState.save_teacher, width="100%", margin_top="1em"),
        spacing="4", width="100%"
    )

# --- Tabs --- #
def tab_gestion_cursos():
    return rx.box(
        rx.hstack(
            rx.heading("Cursos", size="6"), rx.spacer(),
            rx.button("Crear Curso", on_click=AdminState.toggle_course_modal, color_scheme="green"),
            width="100%", mt="4"
        ),
        rx.divider(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("ID"), rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("Profesor Principal"), rx.table.column_header_cell("Profesor Suplente"),
                    rx.table.column_header_cell("Aplicable"), rx.table.column_header_cell("Horario"),
                    rx.table.column_header_cell("Cupos Totales"), rx.table.column_header_cell("Inscritos"),
                    rx.table.column_header_cell("Acciones"),
                )
            ),
            rx.table.body(
                rx.foreach(AdminState.cursos_con_profesores, lambda c: rx.table.row(
                    rx.table.cell(c["id"]), rx.table.cell(c["nombre"]), rx.table.cell(c["profesor_nombre"]),
                    rx.table.cell(c["profesor_suplente_nombre"]), rx.table.cell(c["aplicable"]),
                    rx.table.cell(c["horario"]), rx.table.cell(f"{c['cupos_totales']}"),
                    rx.table.cell(f"{c['inscritos_count']}"),
                    rx.table.cell(rx.hstack(
                        rx.button("✏️", size="2", on_click=lambda: AdminState.editar_curso(c["id"])),
                        rx.button("🗑️", size="2", color_scheme="red", on_click=lambda: AdminState.preparar_eliminacion_curso(c["id"])),
                        spacing="1"
                    )),
                ))
            ),
            width="100%", mt="4"
        ),
    )

def tab_gestion_estudiantes():
    return rx.box(
        rx.hstack(
            rx.heading("Estudiantes", size="6"), rx.spacer(),
            rx.input(placeholder="Buscar por nombre...", on_change=AdminState.set_student_search_query, width="300px"),
            rx.button("Crear Estudiante", on_click=lambda: AdminState.open_student_form(None), color_scheme="green"),
            width="100%", mt="4"
        ),
        rx.divider(),
        rx.table.root(
            rx.table.header(rx.table.row(
                rx.table.column_header_cell("ID"), rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Email"), rx.table.column_header_cell("Nivel"),
                rx.table.column_header_cell("Estado"), rx.table.column_header_cell("Acciones"),
            )),
            rx.table.body(rx.foreach(AdminState.filtered_students, lambda s: rx.table.row(
                rx.table.cell(s.id), rx.table.cell(s.nombre), rx.table.cell(s.email), rx.table.cell(s.nivel),
                rx.table.cell(rx.cond(s.is_active, rx.badge("Activo", color_scheme="green"), rx.badge("Inactivo", color_scheme="gray"))),
                rx.table.cell(rx.hstack(
                    rx.button("✏️", size="2", on_click=lambda: AdminState.open_student_form(s.id)),
                    rx.switch(checked=s.is_active, on_change=lambda is_checked: AdminState.toggle_student_status(s.id, is_checked)),
                    spacing="1"
                )),
            ))),
            width="100%", mt="4"
        ),
    )

def tab_gestion_profesores():
    return rx.box(
        rx.hstack(
            rx.heading("Profesores", size="6"), rx.spacer(),
            rx.input(placeholder="Buscar por nombre...", on_change=AdminState.set_teacher_search_query, width="300px"),
            rx.button("Crear Profesor", on_click=lambda: AdminState.open_teacher_form(None), color_scheme="green"),
            width="100%", mt="4"
        ),
        rx.divider(),
        rx.table.root(
            rx.table.header(rx.table.row(
                rx.table.column_header_cell("ID"), rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Email"), rx.table.column_header_cell("Estado"),
                rx.table.column_header_cell("Acciones"),
            )),
            rx.table.body(rx.foreach(AdminState.filtered_teachers, lambda t: rx.table.row(
                rx.table.cell(t.id), rx.table.cell(t.nombre), rx.table.cell(t.email),
                rx.table.cell(rx.cond(t.is_active, rx.badge("Activo", color_scheme="green"), rx.badge("Inactivo", color_scheme="gray"))),
                rx.table.cell(rx.hstack(
                    rx.button("✏️", size="2", on_click=lambda: AdminState.open_teacher_form(t.id)),
                    rx.switch(checked=t.is_active, on_change=lambda is_checked: AdminState.toggle_teacher_status(t.id, is_checked)),
                    spacing="1"
                )),
            ))),
            width="100%", mt="4"
        ),
    )

# --- Main Admin View --- #
def vista_administrador():
    return PageShell(
        rx.heading("Panel de Administración", size="8", color="white"),
        rx.hstack(
            rx.text("Período de Inscripción:"),
            rx.switch(checked=BaseState.inscripcion_activa, on_change=BaseState.set_inscripcion_activa),
            spacing="4", margin_bottom="1em",
        ),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Cursos", value="cursos"),
                rx.tabs.trigger("Estudiantes", value="estudiantes"),
                rx.tabs.trigger("Profesores", value="profesores"),
            ),
            rx.tabs.content(tab_gestion_cursos(), value="cursos"),
            rx.tabs.content(tab_gestion_estudiantes(), value="estudiantes"),
            rx.tabs.content(tab_gestion_profesores(), value="profesores"),
            defaultValue="cursos", width="100%"
        ),

        # --- Modals ---
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Crear / Editar Curso"),
                FormularioCurso(profesor_nombres=AdminState.profesor_nombres),
                rx.dialog.close(rx.button("Cancelar", variant="soft"))
            ),
            open=AdminState.show_form_modal,
            on_open_change=AdminState.toggle_course_modal
        ),
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.alert_dialog.title("Confirmar Eliminación"),
                rx.alert_dialog.description("¿Estás seguro de que quieres eliminar este curso? Esta acción no se puede deshacer."),
                rx.flex(
                    rx.alert_dialog.cancel(rx.button("Cancelar", variant="soft", color_scheme="gray")),
                    rx.alert_dialog.action(rx.button("Eliminar", color_scheme="red", on_click=AdminState.eliminar_curso)),
                    spacing="3", margin_top="15px", justify="end",
                ),
            ),
            open=AdminState.show_delete_dialog,
            on_open_change=AdminState.cancelar_eliminacion_curso,
        ),
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Crear / Editar Estudiante"),
                student_form(),
                rx.dialog.close(rx.button("Cancelar", variant="soft", on_click=AdminState.close_student_form))
            ),
            open=AdminState.show_student_form,
            on_open_change=AdminState.on_student_form_open_change,
        ),
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Crear / Editar Profesor"),
                teacher_form(),
                rx.dialog.close(rx.button("Cancelar", variant="soft", on_click=AdminState.close_teacher_form))
            ),
            open=AdminState.show_teacher_form,
            on_open_change=AdminState.on_teacher_form_open_change,
        ),
    )

vista_administrador.on_load = BaseState.require_admin
