from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, UserMixin
from flask_login import login_required


from app.controllers.usuario_controller import obtener_usuario_por_username
from app.controllers.estudiante_controller  import obtener_estudiante_por_usuario_id
from app.controllers.profesor_controller  import obtener_profesor_por_usuario_id

auth_bp = Blueprint('auth', __name__)

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

        user_data = obtener_usuario_por_username(username)

        if user_data and check_password_hash(user_data['password_hash'], password):
            if not user_data['activo']:
                flash('Tu cuenta está inactiva. Contacta al administrador.', 'warning')
                return redirect(url_for('auth.login'))

            user = Usuario(user_data)
            login_user(user)

            # Guardar datos adicionales en sesión según el rol
            if user.rol_id == 2:
                est_data = obtener_estudiante_por_usuario_id(user.id)
                session['perfil'] = 'estudiante'
                session['datos_estudiante'] = est_data
            elif user.rol_id == 3:
                prof_data = obtener_profesor_por_usuario_id(user.id)
                session['perfil'] = 'profesor'
                session['datos_profesor'] = prof_data

            # Redirección por rol
            if user.rol_id == 1:
                return redirect(url_for('admin.dashboard'))
            elif user.rol_id == 2:
                return redirect(url_for('estudiante.lista_estudiantes'))
            elif user.rol_id == 3:
                return redirect(url_for('profesor.dashboard'))
            else:
                flash('Rol desconocido', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Limpia la sesión para eliminar datos adicionales
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))