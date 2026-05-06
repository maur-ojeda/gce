import sqlmodel as sm
from . import models
from .models import Curso, Estudiante, Profesor

# Hashing passwords
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Database setup
engine = sm.create_engine("sqlite:///gce.db")

def create_db_and_tables():
    sm.SQLModel.metadata.create_all(engine)

def init_db():
    with sm.Session(engine) as session:
        # Check if tables are empty before populating
        if not session.exec(sm.select(Profesor)).first():
            profesores = [
                Profesor(id=1, nombre="Ana López", email="ana.lopez@example.com", password=get_password_hash("password")),
                Profesor(id=2, nombre="Carlos Pérez", email="carlos.perez@example.com", password=get_password_hash("password")),
                Profesor(id=3, nombre="Laura García", email="laura.garcia@example.com", password=get_password_hash("password")),
                Profesor(id=4, nombre="Miguel Fernández", email="miguel.fernandez@example.com", password=get_password_hash("password")),
                Profesor(id=5, nombre="Sofía Ruiz", email="sofia.ruiz@example.com", password=get_password_hash("password")),
            ]
            session.add_all(profesores)

            estudiantes = [
                Estudiante(id=1, nombre="Juan Pérez", email="juan@test.com", password=get_password_hash("password"), nivel="1er Medio", cursos_inscritos=[1, 3]),
                Estudiante(id=2, nombre="María González", email="maria@test.com", password=get_password_hash("password"), nivel="2do Medio", cursos_inscritos=[2, 3]),
                Estudiante(id=3, nombre="Pedro Ramírez", email="pedro@test.com", password=get_password_hash("password"), nivel="1er Medio", cursos_inscritos=[1, 4]),
                Estudiante(id=4, nombre="Ana Torres", email="ana@test.com", password=get_password_hash("password"), nivel="2do Medio", cursos_inscritos=[2, 5]),
                Estudiante(id=5, nombre="Luis Soto", email="luis@test.com", password=get_password_hash("password"), nivel="1er Medio", cursos_inscritos=[3, 5]),
            ]
            session.add_all(estudiantes)

            cursos = [
                Curso(id=1, nombre="Intro Programación", profesor_id=1, cupos_totales=20,
                      descripcion="Fundamentos de programación", aplicable="1er Medio", horario="Lunes 15:00-16:30",
                      estudiantes_inscritos=[1, 3]),
                Curso(id=2, nombre="Matemáticas Avanzadas", profesor_id=2, cupos_totales=15,
                      descripcion="Cálculo y álgebra lineal", aplicable="2do Medio", horario="Martes 10:00-11:30",
                      estudiantes_inscritos=[2, 4]),
                Curso(id=3, nombre="Historia Universal", profesor_id=3, cupos_totales=25,
                      descripcion="Desde la antigüedad hasta hoy", aplicable="1er Medio", horario="Miércoles 09:00-10:30",
                      estudiantes_inscritos=[1, 2, 5]),
                Curso(id=4, nombre="Física Cuántica", profesor_id=4, cupos_totales=10,
                      descripcion="Principios de la mecánica cuántica", aplicable="3er Medio", horario="Jueves 14:00-15:30",
                      estudiantes_inscritos=[3]),
                Curso(id=5, nombre="Literatura Clásica", profesor_id=5, cupos_totales=18,
                      descripcion="Análisis de obras literarias", aplicable="2do Medio", horario="Viernes 11:00-12:30",
                      estudiantes_inscritos=[4, 5]),
                Curso(id=6, nombre="Química Orgánica", profesor_id=1, profesor_suplente_id=2, cupos_totales=12,
                      descripcion="Estudio de compuestos de carbono", aplicable="3er Medio", horario="Lunes 09:00-10:30",
                      estudiantes_inscritos=[]),
                Curso(id=7, nombre="Programación Web", profesor_id=3, cupos_totales=10,
                      descripcion="Desarrollo de aplicaciones web", aplicable="2do Medio", horario="Martes 14:00-15:30",
                      estudiantes_inscritos=[2]),
                Curso(id=8, nombre="Diseño Gráfico", profesor_id=4, profesor_suplente_id=5, cupos_totales=8,
                      descripcion="Principios de diseño visual", aplicable="1er Medio", horario="Miércoles 11:00-12:30",
                      estudiantes_inscritos=[]),
                Curso(id=9, nombre="Economía Global", profesor_id=5, cupos_totales=20,
                      descripcion="Análisis de mercados internacionales", aplicable="3er Medio", horario="Jueves 10:00-11:30",
                      estudiantes_inscritos=[]),
                Curso(id=10, nombre="Filosofía Antigua", profesor_id=1, cupos_totales=15,
                      descripcion="Pensadores griegos y romanos", aplicable="1er Medio", horario="Viernes 09:00-10:30",
                      estudiantes_inscritos=[]),
            ]
            session.add_all(cursos)
            session.commit()
        else:
            

