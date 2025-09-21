import reflex as rx
import sqlmodel as sm
import sqlalchemy as sa

class Profesor(sm.SQLModel, table=True):
    id: int | None = sm.Field(default=None, primary_key=True)
    nombre: str

class Estudiante(sm.SQLModel, table=True):
    id: int | None = sm.Field(default=None, primary_key=True)
    nombre: str
    email: str = sm.Field(unique=True, index=True)
    password: str
    nivel: str
    cursos_inscritos: list[int] = sm.Field(default=[], sa_column=sa.Column(sa.JSON))

class Curso(sm.SQLModel, table=True):
    id: int | None = sm.Field(default=None, primary_key=True)
    nombre: str
    profesor_id: int
    profesor_suplente_id: int | None = None
    cupos_totales: int
    descripcion: str
    aplicable: str
    horario: str
    estudiantes_inscritos: list[int] = sm.Field(default=[], sa_column=sa.Column(sa.JSON))
    