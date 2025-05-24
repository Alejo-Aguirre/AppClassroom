from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.controllers.estudiante_controller import (
    listar_estudiantes,
    crear_estudiante,
    obtener_estudiante_por_id,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    
)

estudiante_bp = Blueprint('estudiante', __name__)

# Página principal (home)
@estudiante_bp.route('/')
def index():
    return render_template('index.html')

# Lista de estudiantes con tabla
@estudiante_bp.route('/estudiantes')
def lista_estudiantes():
    estudiantes = listar_estudiantes()
    return render_template('estudiantes.html', estudiantes=estudiantes)

# Formulario para crear estudiante
@estudiante_bp.route('/estudiantes/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        numero_identificacion = request.form['numero_identificacion']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        username = request.form['username']
        password = request.form['password']
        activo = True  # o usa: request.form.get('activo') == 'on'
        rol_id = 2  # Rol estudiante

        # Datos de estudiante
        nivel_educativo = request.form['nivel_educativo']
        institucion_educativa = request.form['institucion_educativa']
        carrera_area_estudio = request.form['carrera_area_estudio']
        fecha_ingreso = request.form['fecha_ingreso']

        # Timestamp actual
        now = datetime.now()

        # Encriptar contraseña (opcional si ya está encriptada antes)
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash(password)

        # Crear el estudiante
        crear_estudiante(
            numero_identificacion, nombre, apellido, email, telefono,
            username, password_hash, activo, rol_id,
            now, now,
            nivel_educativo, institucion_educativa,
            carrera_area_estudio, fecha_ingreso
        )

        return redirect(url_for('estudiante.lista_estudiantes'))

    return render_template('create_estudiante.html')



@estudiante_bp.route('/estudiantes/buscar', methods=['GET'])
def buscar():
    termino = request.args.get('buscar', '').strip()
    if termino:
        estudiantes = buscar_estudiantes(termino)
    else:
        estudiantes = listar_estudiantes()
    return render_template('estudiantes.html', estudiantes=estudiantes)


# Formulario para editar estudiante
@estudiante_bp.route('/estudiantes/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    estudiante = obtener_estudiante_por_id(id)
    if not estudiante:
        flash("Estudiante no encontrado", "danger")
        return redirect(url_for('estudiante.lista_estudiantes'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        edad = request.form['edad']
        actualizar_estudiante(id, nombre, email, edad)
        flash("Estudiante actualizado correctamente", "success")
        return redirect(url_for('estudiante.lista_estudiantes'))

    return render_template('edit_estudiante.html', estudiante=estudiante)

# Ruta para eliminar estudiante (POST para seguridad)
@estudiante_bp.route('/estudiantes/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminado = eliminar_estudiante(id)
    if eliminado:
        flash("Estudiante eliminado correctamente", "success")
    else:
        flash("Error al eliminar estudiante", "danger")
    return redirect(url_for('estudiante.lista_estudiantes'))


