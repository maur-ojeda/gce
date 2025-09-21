import reflex as rx
import sqlmodel as sm
from .ui import UIState
from .base import get_session
from ..models import Curso, Estudiante, AuditLog, Profesor
from ..database import get_password_hash

class AdminState(UIState):
    # --- SHARED STATE ---
    show_delete_dialog: bool = False

    # --- COURSE MANAGEMENT STATE ---
    curso_editando: int = -1
    nombre: str = ""
    profesor_id: str = ""
    profesor_suplente_id: str = ""
    aplicable: str = ""
    horario: str = ""
    cupos_totales: int = 0
    descripcion: str = ""
    curso_a_eliminar: int = -1

    # --- STUDENT MANAGEMENT STATE ---
    editing_student_id: int | None = None
    show_student_form: bool = False
    student_search_query: str = ""
    student_list_version: int = 0
    student_nombre: str = ""
    student_email: str = ""
    student_nivel: str = ""
    student_password: str = ""

    #<editor-fold desc="COURSE MANAGEMENT METHODS">
    def set_nombre(self, value: str): self.nombre = value
    def set_profesor_id(self, value: str): self.profesor_id = value
    def set_profesor_suplente_id(self, value: str): self.profesor_suplente_id = value
    def set_aplicable(self, value: str): self.aplicable = value
    def set_horario(self, value: str): self.horario = value
    def set_descripcion(self, value: str): self.descripcion = value
    def set_cupos_totales(self, value: str):
        try:
            self.cupos_totales = int(value)
        except (ValueError, TypeError):
            self.cupos_totales = 0

    def _clear_course_form(self):
        self.nombre, self.profesor_id, self.profesor_suplente_id, self.aplicable, self.horario, self.descripcion = "", "", "", "", "", ""
        self.cupos_totales, self.curso_editando = 0, -1

    def toggle_course_modal(self):
        self.show_form_modal = not self.show_form_modal
        if not self.show_form_modal:
            self._clear_course_form()

    def editar_curso(self, curso_id: int):
        with get_session() as session:
            curso = session.get(Curso, curso_id)
            if curso:
                self.curso_editando = curso_id
                self.nombre = curso.nombre
                self.profesor_id = next((p.nombre for p in self.profesores if p.id == curso.profesor_id), "")
                self.profesor_suplente_id = next((p.nombre for p in self.profesores if p.id == curso.profesor_suplente_id), "")
                self.aplicable, self.horario, self.cupos_totales, self.descripcion = curso.aplicable, curso.horario, curso.cupos_totales, curso.descripcion
        self.toggle_course_modal()

    def guardar_curso(self):
        with get_session() as session:
            prof_id = next((p.id for p in self.profesores if p.nombre == self.profesor_id), None)
            prof_supl_id = next((p.id for p in self.profesores if p.nombre == self.profesor_suplente_id), None)
            if self.curso_editando == -1:
                curso = Curso(nombre=self.nombre, profesor_id=prof_id, profesor_suplente_id=prof_supl_id, cupos_totales=self.cupos_totales, descripcion=self.descripcion, aplicable=self.aplicable, horario=self.horario, estudiantes_inscritos=[])
                session.add(curso)
            else:
                curso = session.get(Curso, self.curso_editando)
                if curso:
                    curso.nombre, curso.profesor_id, curso.profesor_suplente_id, curso.cupos_totales, curso.descripcion, curso.aplicable, curso.horario = self.nombre, prof_id, prof_supl_id, self.cupos_totales, self.descripcion, self.aplicable, self.horario
                    session.add(curso)
            session.commit()
        self.toggle_course_modal()

    def preparar_eliminacion_curso(self, curso_id: int):
        self.curso_a_eliminar, self.show_delete_dialog = curso_id, True

    def cancelar_eliminacion_curso(self):
        self.curso_a_eliminar, self.show_delete_dialog = -1, False

    def eliminar_curso(self):
        with get_session() as session:
            curso = session.get(Curso, self.curso_a_eliminar)
            if curso and curso.estudiantes_inscritos:
                self.cancelar_eliminacion_curso()
                return rx.window_alert("No se puede eliminar el curso porque tiene estudiantes inscritos.")
            if curso:
                session.delete(curso)
                session.commit()
        self.cancelar_eliminacion_curso()

    @rx.var
    def course_form_is_valid(self) -> bool:
        return all([self.nombre, self.profesor_id, self.aplicable, self.horario, self.cupos_totales > 0, self.descripcion])
    #</editor-fold>

    #<editor-fold desc="STUDENT MANAGEMENT METHODS">
    @rx.var
    def filtered_students(self) -> list[Estudiante]:
        _ = self.student_list_version
        with get_session() as session:
            query = sm.select(Estudiante)
            if self.student_search_query:
                query = query.where(Estudiante.nombre.contains(self.student_search_query))
            return session.exec(query.order_by(Estudiante.id)).all()

    def set_student_search_query(self, query: str): self.student_search_query = query
    def set_student_nombre(self, value: str): self.student_nombre = value
    def set_student_email(self, value: str): self.student_email = value
    def set_student_nivel(self, value: str): self.student_nivel = value
    def set_student_password(self, value: str): self.student_password = value

    def _clear_student_form(self):
        self.editing_student_id, self.student_nombre, self.student_email, self.student_nivel, self.student_password = None, "", "", "", ""

    def open_student_form(self, student_id: int | None = None):
        self._clear_student_form()
        if student_id:
            self.editing_student_id = student_id
            with get_session() as session:
                student = session.get(Estudiante, student_id)
                if student:
                    self.student_nombre, self.student_email, self.student_nivel = student.nombre, student.email, student.nivel
        self.show_student_form = True

    def close_student_form(self):
        self.show_student_form = False
        self._clear_student_form()

    def save_student(self):
        with get_session() as session:
            action, details = "", {}
            if self.editing_student_id:
                student = session.get(Estudiante, self.editing_student_id)
                if student:
                    action = "UPDATE_STUDENT"
                    details = {"old": student.dict(), "new": {"nombre": self.student_nombre, "nivel": self.student_nivel, "email": self.student_email}}
                    student.nombre, student.email, student.nivel = self.student_nombre, self.student_email, self.student_nivel
                    if self.student_password:
                        student.password = get_password_hash(self.student_password)
                    session.add(student)
            else:
                action = "CREATE_STUDENT"
                password = self.student_password if self.student_password else "defaultpassword"
                student = Estudiante(nombre=self.student_nombre, email=self.student_email, nivel=self.student_nivel, password=get_password_hash(password))
                details = {"new": student.dict()}
                session.add(student)
            session.flush()
            log = AuditLog(actor_id=self.usuario_actual_id, action=action, target_entity="Estudiante", target_id=student.id, details=details)
            session.add(log)
            session.commit()
        self.close_student_form()
        self.student_list_version += 1

    def toggle_student_status(self, student_id: int, is_active: bool):
        with get_session() as session:
            student = session.get(Estudiante, student_id)
            if student:
                student.is_active = is_active
                action = "REACTIVATE_STUDENT" if is_active else "ARCHIVE_STUDENT"
                details = {"old_is_active": not is_active, "new_is_active": is_active}
                log = AuditLog(actor_id=self.usuario_actual_id, action=action, target_entity="Estudiante", target_id=student.id, details=details)
                session.add(student)
                session.add(log)
                session.commit()
        self.student_list_version += 1

    def on_student_form_open_change(self, is_open: bool):
        if not is_open:
            self.close_student_form()
    #</editor-fold>
