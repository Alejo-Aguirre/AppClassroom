from app.models.usuario import UsuarioModel

model = UsuarioModel()

def obtener_usuario_por_username(username):
    return model.obtener_por_username(username)

def obtener_usuario_por_id(id):
    return model.obtener_por_id(id)
