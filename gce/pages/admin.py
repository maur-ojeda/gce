# pages/admin.py
import reflex as rx
from ..state import State
from ..components.forms import formulario_curso
from ..components.navbar import navbar

def vista_administrador():
    """Interfaz para que el administrador gestione los cursos."""
    # Elimina el rx.cond del nivel superior
    return rx.vstack(
        navbar(),
        rx.center(
            rx.heading("Panel de Administración de Cursos", color="white", font_size="2em"),
        ),
        rx.container(                   
            rx.hstack(
                rx.heading("Cursos Existentes", size="8"),
                rx.spacer(),
                rx.button(
                    "Crear Nuevo Curso",
                    on_click=State.toggle_form_modal,
                    color_scheme="green"
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
                            rx.table.column_header_cell("Nivel"),
                            rx.table.column_header_cell("Horario"),
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
                                rx.table.cell(curso["aplicable"]),
                                rx.table.cell(curso["horario"]),
                                rx.table.cell(f"{curso['cupos_totales']}"),
                                rx.table.cell(f"{curso['inscritos_count']}"),                                                                    
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button(
                                            "✏️",
                                            on_click=lambda c=curso: State.seleccionar_curso_para_editar(c["id"]),
                                            color_scheme="blue",
                                            size="2"
                                        ),
                                        rx.button(
                                            "🗑️", 
                                            color_scheme="red",
                                            size="2",
                                            on_click=lambda c=curso: State.solicitar_eliminacion_curso(c["id"])
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
        
        # Modal de formulario
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        State.curso_seleccionado != -1,
                        "Editar Curso",
                        "Crear Nuevo Curso"
                    )
                ),
                formulario_curso(),
                
                rx.dialog.close(
                    rx.button(
                        "Cancelar",                
                        margin_top="1rem",
                        variant="soft"
                    )
                )
            ),
            open=State.show_form_modal,
            on_open_change=State.toggle_form_modal
        ),
        
        # Modal de confirmación de eliminación
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.alert_dialog.title("Confirmar Eliminación"),
                rx.alert_dialog.description(
                    "¿Está seguro que desea eliminar este curso? Esta acción no se puede deshacer."
                ),
                rx.flex(
                    rx.alert_dialog.cancel(
                        rx.button("Cancelar", variant="soft", color_scheme="gray")
                    ),
                    rx.alert_dialog.action(
                        rx.button(
                            "Eliminar", 
                            color_scheme="red",
                            on_click=State.eliminar_curso_confirmado
                        )
                    ),
                    spacing="3",
                    margin_top="16px"
                )
            ),
            open=State.mostrar_confirmacion_eliminacion,
            on_open_change=State.toggle_confirmacion_eliminacion
        ),
        
        # Mensajes de éxito/error
        rx.cond(
            State.mensaje_exito != "",
            rx.callout(
                State.mensaje_exito,
                icon="check",
                color_scheme="green",
                role="alert",
                margin_top="1rem"
            ),
            rx.fragment()
        ),
        rx.cond(
            State.mensaje_error != "",
            rx.callout(
                State.mensaje_error,
                icon="triangle_alert",
                color_scheme="red",
                role="alert",
                margin_top="1rem"
            ),
            rx.fragment()
        ),
        
        bg="#0066cc",
        padding="20px",
        width="100%",
    )