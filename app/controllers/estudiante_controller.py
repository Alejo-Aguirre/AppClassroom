from app.models.estudiante import EstudianteModel

model = EstudianteModel()


def listar_estudiantes():
    return model.fetch_all()

def obtener_estudiante_por_id(id):
    return model.fetch_by_id(id)

def buscar_estudiantes(termino):
    return model.search(termino)

def crear_estudiante(numero_identificacion, nombre, apellido, email, telefono,
                     username, password_hash, activo, rol_id,
                     created_at, updated_at,
                     nivel_educativo, institucion_educativa,
                     carrera_area_estudio, fecha_ingreso):
    return model.create(numero_identificacion, nombre, apellido, email, telefono,
                        username, password_hash, activo, rol_id,
                        created_at, updated_at,
                        nivel_educativo, institucion_educativa,
                        carrera_area_estudio, fecha_ingreso)

def actualizar_estudiante(id, nombre, email, edad):
    return model.update(id, nombre, email, edad)

def eliminar_estudiante(id):
    return model.delete(id)

def obtener_estudiante_por_usuario_id(usuario_id):
    return model.obtener_por_usuario_id(usuario_id)

