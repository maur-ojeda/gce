import reflex as rx
from pydantic import Field 

class Profesor(rx.Base):
    id: int
    nombre: str

class Estudiante(rx.Base):
    id: int
    nombre: str
    nivel: str
    cursos_inscritos: list[int] = Field(default_factory=list)


class Curso(rx.Base):
    id: int
    nombre: str
    profesor_id: int
    cupos_totales: int
    descripcion: str
    aplicable: str
    horario: str
    estudiantes_inscritos: list[int] = Field(default_factory=list)
    