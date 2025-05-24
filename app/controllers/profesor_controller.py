from app.models.profesor import ProfesorModel

model = ProfesorModel()

def listar_profesores():
    return model.fetch_all()

def obtener_profesor_por_id(id):
    return model.fetch_by_id(id)

def buscar_profesores(termino):
    return model.search(termino)

def crear_profesor(numero_identificacion, nombre, apellido, email, telefono,
                   username, password_hash, activo, rol_id,
                   created_at, updated_at,
                   especialidad, experiencia, fecha_contratacion):
    return model.create(numero_identificacion, nombre, apellido, email, telefono,
                        username, password_hash, activo, rol_id,
                        created_at, updated_at,
                        especialidad, experiencia, fecha_contratacion)

def actualizar_profesor(id, nombre, email, edad):
    return model.update(id, nombre, email, edad)

def eliminar_profesor(id):
    return model.delete(id)

def obtener_profesor_por_usuario_id(usuario_id):
    return model.obtener_por_usuario_id(usuario_id)
