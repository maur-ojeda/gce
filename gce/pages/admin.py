import reflex as rx
from ..state import State
from ..components.navbar import navbar
from ..components.forms import formulario_curso

# --- Vista del Administrador ---
def vista_administrador():
    """Interfaz para que el administrador gestione los cursos."""
    return rx.vstack(
        rx.box(
            rx.text("Debug cursos en consola"),
            on_mount=rx.console_log([
                'Profesores', State.profesores, 
                'cursos', State.cursos
            ]),
        ),

        rx.center(
            rx.heading("Panel de Administración de Cursos", color="white", font_size="2em"),
        ),
        rx.container(                   
            rx.hstack(
                rx.heading("Cursos Existentes", size="8"),
                rx.spacer(),
                rx.button(
                    "Crear Nuevo Curso",
                    on_click=State.toggle_form_modal                    
                ),
                width="100%",
                margin_top="20px"
            ),
            rx.divider(),
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(                            
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Nombre"),
                            rx.table.column_header_cell("Profesor"),
                            rx.table.column_header_cell("Cupos"),
                            rx.table.column_header_cell("Inscritos"),
                            rx.table.column_header_cell("Acciones"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            State.cursos_con_profesores,
                            lambda curso:
                            rx.table.row(
                                rx.table.cell(curso["id"]),                                    
                                rx.table.cell(curso["nombre"]),
                                rx.table.cell(curso["profesor_nombre"]),  
                                rx.table.cell(f"{curso['cupos_totales']}"),
                                rx.table.cell(f"{curso['inscritos_count']}"),                                                                    
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button(
                                            "✏️",
                                            on_click=lambda c=curso: State.seleccionar_curso_para_editar(c["id"]),
                                            color_scheme="blue"
                                        ),
                                        rx.button(
                                            "🗑️", 
                                            color_scheme="red",
                                            on_click=lambda c=curso: State.eliminar_curso(c["id"])
                                        ),
                                        spacing="1"
                                    )
                                ),
                            ),                        
                        )
                    ),
                    width="100%",
                )
            ),
        ),
        
        # === MODAL DE FORMULARIO ===
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        State.curso_seleccionado == -1,
                        "Crear Nuevo Curso",
                        "Editar Curso"
                    )
                ),
                rx.dialog.description(
                    "This is a dialog component. You can render anything you want in here.",
                    padding="1em 0",                         
                ),
                formulario_curso(),                
            ),
            open=State.show_form_modal,
            on_open_change=State.toggle_form_modal
        ),        
        padding="20px",
        width="100%",
    )