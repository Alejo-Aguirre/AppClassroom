from flask import Flask
from flask_login import LoginManager
from app.routes.estudiante_routes import estudiante_bp
from app.routes.api_estudiante_routes import api_bp 
from app.routes.auth_routes import auth_bp
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Establecer secret key desde variable de entorno
app.secret_key = os.getenv("SECRET_KEY", "clave_insegura_por_defecto")

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Importa la clase Usuario (UserMixin) que usas para login
from app.routes.auth_routes import Usuario
from app.models.usuario import UsuarioModel

@login_manager.user_loader
def load_user(user_id):
    usuario_model = UsuarioModel()
    user_data = usuario_model.obtener_por_id(user_id)  # Necesitas implementar este método
    if user_data:
        return Usuario(user_data)
    return None

# Registrar blueprints
app.register_blueprint(estudiante_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)  # registramos el blueprint del API


#cuando se vaya a correr en la mv app.run(host='0.0.0.0', port=5000, debug=True) 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
