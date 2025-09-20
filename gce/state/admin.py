import reflex as rx
from .ui import UIState
from ..models import Curso

class AdminState(UIState):
    curso_editando: int = -1
    nombre: str = ""
    profesor_id: str = ""
    profesor_suplente_id: str = "" # Add this line
    aplicable: str = ""
    horario: str = ""
    cupos_totales: int = 0
    descripcion: str = ""
    show_delete_dialog: bool = False
    curso_a_eliminar: int = -1

    def set_nombre(self, value: str):
        self.nombre = value

    def set_profesor_id(self, value: str):
        self.profesor_id = value

    def set_profesor_suplente_id(self, value: str): # Add this method
        self.profesor_suplente_id = value

    def set_aplicable(self, value: str):
        self.aplicable = value

    def set_horario(self, value: str):
        self.horario = value

    def set_cupos_totales(self, value: str):
        try:
            self.cupos_totales = int(value)
        except (ValueError, TypeError):
            self.cupos_totales = 0

    def set_descripcion(self, value: str):
        self.descripcion = value

    def _clear_form(self):
        self.nombre = ""
        self.profesor_id = ""
        self.profesor_suplente_id = "" # Clear this
        self.aplicable = ""
        self.horario = ""
        self.cupos_totales = 0
        self.descripcion = ""

    def toggle_modal(self):
        self.show_form_modal = not self.show_form_modal
        if not self.show_form_modal:
            self.curso_editando = -1
            self._clear_form()

    def editar(self, curso_id: int):
        curso = next((c for c in self.cursos if c.id == curso_id), None)
        if curso:
            self.curso_editando = curso_id
            self.nombre = curso.nombre
            profesor = next((p for p in self.profesores if p.id == curso.profesor_id), None)
            if profesor:
                self.profesor_id = profesor.nombre
            else:
                self.profesor_id = "" # Clear if not found

            # Populate substitute professor
            if curso.profesor_suplente_id:
                profesor_suplente = next((p for p in self.profesores if p.id == curso.profesor_suplente_id), None)
                if profesor_suplente:
                    self.profesor_suplente_id = profesor_suplente.nombre
                else:
                    self.profesor_suplente_id = ""
            else:
                self.profesor_suplente_id = ""

            self.aplicable = curso.aplicable
            self.horario = curso.horario
            self.cupos_totales = curso.cupos_totales
            self.descripcion = curso.descripcion
        self.toggle_modal()

    def guardar(self):
        profesor_id = next(
            (p.id for p in self.profesores if p.nombre == self.profesor_id),
            None # Use None if not found
        )
        profesor_suplente_id = next( # Add this
            (p.id for p in self.profesores if p.nombre == self.profesor_suplente_id),
            None # Use None if not found
        )

        if self.curso_editando == -1:  # CREAR
            nuevo_id = max((c.id for c in self.cursos), default=0) + 1
            self.cursos.append(Curso(
                id=nuevo_id,
                nombre=self.nombre,
                profesor_id=profesor_id,
                profesor_suplente_id=profesor_suplente_id, # Add this
                cupos_totales=self.cupos_totales,
                descripcion=self.descripcion,
                aplicable=self.aplicable,
                horario=self.horario,
                estudiantes_inscritos=[]
            ))
        else:  # EDITAR
            curso = next(c for c in self.cursos if c.id == self.curso_editando)
            curso.nombre = self.nombre
            curso.profesor_id = profesor_id
            curso.profesor_suplente_id = profesor_suplente_id, # Add this
            curso.cupos_totales = self.cupos_totales
            curso.descripcion = self.descripcion
            curso.aplicable = self.aplicable
            curso.horario = self.horario
        self.toggle_modal()

    def preparar_eliminacion(self, curso_id: int):
        self.curso_a_eliminar = curso_id
        self.show_delete_dialog = True

    def cancelar_eliminacion(self):
        self.curso_a_eliminar = -1
        self.show_delete_dialog = False

    def eliminar(self):
        curso_id = self.curso_a_eliminar
        curso = next((c for c in self.cursos if c.id == curso_id), None)
        if curso and curso.estudiantes_inscritos:
            self.cancelar_eliminacion()
            return rx.window_alert("No se puede eliminar el curso porque tiene estudiantes inscritos.")

        for est in self.estudiantes:
            if curso_id in est.cursos_inscritos:
                est.cursos_inscritos.remove(curso_id)
        self.cursos = [c for c in self.cursos if c.id != curso_id]
        self.cancelar_eliminacion()