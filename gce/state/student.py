import reflex as rx
from .ui import UIState
from ..models import Curso

MAX_CURSOS_INSCRITOS = 3 # Define the maximum number of courses

class StudentState(UIState):
    mensaje: str = ""
    show_success_modal: bool = False
    show_inscribir_button_in_modal: bool = False # Add this

    def mostrar_detalle(self, curso_id: int):
        self.detalle_curso_id = curso_id
        # Determine if the "Inscribirme" button should be shown in the modal
        curso = next((c for c in self.cursos_con_profesores if c["id"] == curso_id), None)
        if curso:
            # Check if the course is in cursos_disponibles
            # This logic is similar to how cursos_disponibles is computed
            est = self.estudiante_actual
            self.show_inscribir_button_in_modal = (
                curso["aplicable"] == est.nivel
                and curso["id"] not in est.cursos_inscritos
                and curso["cupos_disponibles"] > 0
            )
        else:
            self.show_inscribir_button_in_modal = False

        self.toggle_detalle()

    def _parse_horario(self, horario_str: str) -> tuple[str, int, int]:
        # Example: "Lunes 15:00-16:30" -> ("Lunes", 1500, 1630)
        parts = horario_str.split(" ")
        day = parts[0]
        time_range = parts[1].split("-")
        start_time = int(time_range[0].replace(":", ""))
        end_time = int(time_range[1].replace(":", ""))
        return day, start_time, end_time

    def _horario_solapado(self, horario1: str, horario2: str) -> bool:
        day1, start1, end1 = self._parse_horario(horario1)
        day2, start2, end2 = self._parse_horario(horario2)

        if day1 != day2:
            return False # Different days, no overlap

        # Check for overlap
        # [start1, end1] and [start2, end2]
        # Overlap if (start1 < end2 and start2 < end1)
        return max(start1, start2) < min(end1, end2)


    def _validar_inscripcion(self, curso: Curso) -> str | None:
        est = self.estudiante_actual
        if curso.aplicable != est.nivel:
            return f"Solo para {curso.aplicable}"
        if len(curso.estudiantes_inscritos) >= curso.cupos_totales:
            return "Sin cupos"
        if est.id in curso.estudiantes_inscritos:
            return "Ya inscrito"

        # Validate maximum number of courses
        if len(est.cursos_inscritos) >= MAX_CURSOS_INSCRITOS:
            return f"Ya estás inscrito en el máximo de {MAX_CURSOS_INSCRITOS} cursos."

        # Validate schedule conflicts
        for inscrito_id in est.cursos_inscritos:
            curso_inscrito = next((c for c in self.cursos if c.id == inscrito_id), None)
            if curso_inscrito and self._horario_solapado(curso.horario, curso_inscrito.horario):
                return f"Conflicto de horario con {curso_inscrito.nombre}."

        return None

    def inscribir(self, curso_id: int):
        curso = next((c for c in self.cursos if c.id == curso_id), None)
        if not curso:
            self.mensaje = "Curso no encontrado"
            return
        if err := self._validar_inscripcion(curso):
            self.mensaje = err
            # Do not close the detail modal if there's an error
            return
        curso.estudiantes_inscritos.append(self.estudiante_actual.id)
        self.estudiante_actual.cursos_inscritos.append(curso_id)
        self.mensaje = f"¡Inscrito en {curso.nombre}!"
        self.show_success_modal = True # Show success modal
        self.show_detalle_modal = False # Explicitly close detail modal

    def cerrar_modal_exito(self):
        self.show_success_modal = False
        self.mensaje = "" # Clear message
        self.detalle_curso_id = -1 # Reset detail modal state

    @rx.var(cache=True)
    def cursos_disponibles(self) -> list[dict]:
        est = self.estudiante_actual
        return [
            c for c in self.cursos_con_profesores
            if c["aplicable"] == est.nivel
            and c["id"] not in est.cursos_inscritos
            and c["cupos_disponibles"] > 0
        ]

    @rx.var(cache=True)
    def cursos_inscritos(self) -> list[dict]:
        est = self.estudiante_actual
        return [c for c in self.cursos_con_profesores if c["id"] in est.cursos_inscritos]
