import reflex as rx
import sqlmodel as sm
from contextlib import contextmanager
from ..models import Curso, Profesor, Estudiante
from ..database import engine

@contextmanager
def get_session():
    session = sm.Session(engine)
    try:
        yield session
    finally:
        session.close()

# ---------- 1. BASE STATE (datos y helpers comunes) ----------
class BaseState(rx.State):
    usuario_actual_id: int = 1
    rol_actual: str = ""
    inscripcion_activa: bool = True # Keep this

    # HELPERS / VARS
    @rx.var(cache=True)
    def cursos(self) -> list[Curso]:
        with get_session() as session:
            return session.exec(sm.select(Curso)).all()

    @rx.var(cache=True)
    def profesores(self) -> list[Profesor]:
        with get_session() as session:
            return session.exec(sm.select(Profesor)).all()

    @rx.var(cache=True)
    def estudiantes(self) -> list[Estudiante]:
        with get_session() as session:
            return session.exec(sm.select(Estudiante)).all()

    @rx.var(cache=True)
    def profesor_map(self) -> dict[int, str]:
        return {p.id: p.nombre for p in self.profesores}

    @rx.var(cache=True)
    def profesor_nombres(self) -> list[str]:
        return [p.nombre for p in self.profesores]

    @rx.var(cache=True)
    def estudiante_actual(self) -> Estudiante:
        with get_session() as session:
            student = session.get(Estudiante, self.usuario_actual_id)
            if student:
                return student
            return Estudiante(id=0, nombre="Invitado", email="", password="", nivel="", cursos_inscritos=[])

    @rx.var(cache=True)
    def cursos_con_profesores(self) -> list[dict]:
        with get_session() as session:
            cursos = session.exec(sm.select(Curso)).all()
            profesores = {p.id: p.nombre for p in session.exec(sm.select(Profesor)).all()}
            return [
                {
                    **curso.dict(),
                    "profesor_nombre": profesores.get(curso.profesor_id, "Desconocido"),
                    "profesor_suplente_nombre": profesores.get(curso.profesor_suplente_id, "N/A") if curso.profesor_suplente_id else "N/A",
                    "inscritos_count": len(curso.estudiantes_inscritos),
                    "cupos_disponibles": curso.cupos_totales - len(curso.estudiantes_inscritos)
                }
                for curso in cursos
            ]

    @rx.var
    def is_authenticated(self) -> bool:
        return self.rol_actual != ""

    def set_inscripcion_activa(self, value: bool):
        print(f"set_inscripcion_activa called with: {value}") # Add this line
        self.inscripcion_activa = value

    # MÉTODOS COMUNES
    def login(self, rol: str):
        self.rol_actual = rol
        if rol == "administrador":
            return rx.redirect("/admin")
        elif rol == "estudiante":
            return rx.redirect("/estudiante")

    def logout(self):
        self.rol_actual = ""
        self.usuario_actual_id = 1
        return rx.redirect("/login")

    def require_admin(self):
        if not self.is_authenticated or self.rol_actual != "administrador":
            return rx.redirect("/login")

    def require_student(self):
        if not self.is_authenticated or self.rol_actual != "estudiante":
            return rx.redirect("/login")

    def cambiar_rol(self, nuevo: str):
        self.rol_actual = nuevo
        if nuevo == "administrador":
            return rx.redirect("/admin")
        elif nuevo == "estudiante":
            return rx.redirect("/estudiante")
