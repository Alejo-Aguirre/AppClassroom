from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, UserMixin

from app.models.usuario import UsuarioModel
from app.models.estudiante import EstudianteModel
from app.models.profesor import ProfesorModel

auth_bp = Blueprint('auth', __name__)

# Clase auxiliar de usuario para Flask-Login
class Usuario(UserMixin):
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.nombre = data['nombre']
        self.email = data['email']
        self.rol_id = data['rol_id']
        self.activo = data['activo']

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol = int(request.form['rol'])

        print("Intentando login con usuario:", username)
        print("Rol ingresado:", rol)

        usuario_model = UsuarioModel()
        user_data = usuario_model.obtener_por_username(username)
        print("User data desde BD:", user_data)


        if not user_data:
            print("No se encontró el usuario en la base de datos.")
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('login.html')

        print("Usuario encontrado:", user_data)
        print("Rol en BD:", user_data['rol_id'])

        if not check_password_hash(user_data['password_hash'], password):
            print("La contraseña no coincide.")
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('login.html')

        if user_data['rol_id'] != rol:
            print("Rol incorrecto. Rol esperado:", user_data['rol_id'])
            flash('Rol incorrecto para este usuario', 'danger')
            return render_template('login.html')

        print("Login exitoso. Rol correcto:", rol)

        user = Usuario(user_data)
        login_user(user)

        if user.rol_id == 2:
            estudiante_model = EstudianteModel()
            est_data = estudiante_model.obtener_por_usuario_id(user.id)
            session['perfil'] = 'estudiante'
            session['datos_estudiante'] = est_data
        elif user.rol_id == 3:
            profesor_model = ProfesorModel()
            prof_data = profesor_model.obtener_por_usuario_id(user.id)
            session['perfil'] = 'profesor'
            session['datos_profesor'] = prof_data

        if user.rol_id == 1:
            return redirect(url_for('admin.dashboard'))
        elif user.rol_id == 2:
            return redirect(url_for('estudiante.lista_estudiantes'))
        elif user.rol_id == 3:
            return redirect(url_for('profesor.dashboard'))
        else:
            flash('Rol desconocido', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')
