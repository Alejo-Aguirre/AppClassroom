from flask import Blueprint
from flask_restx import Api, Resource, fields, Namespace
from app.controllers.estudiante_controller import listar_estudiantes, crear_estudiante, obtener_estudiante_por_id

# Crea el blueprint
api_bp = Blueprint('api_estudiante', __name__, url_prefix='/api/estudiantes')

# Crea el objeto Api con descripción general
api = Api(api_bp, version='1.0', title='API Estudiantes', description='API para gestión de estudiantes')

# Crea un namespace para organizar los endpoints
estudiante_ns = Namespace('Estudiantes', description='Operaciones relacionadas con estudiantes')
api.add_namespace(estudiante_ns)

# Modelo de estudiante
estudiante_model = estudiante_ns.model('Estudiante', {
    'id': fields.Integer(readonly=True, description='ID del estudiante'),
    'nombre': fields.String(required=True, description='Nombre del estudiante'),
    'email': fields.String(required=True, description='Email del estudiante'),
    'edad': fields.Integer(required=True, description='Edad del estudiante'),
})

# Rutas
@estudiante_ns.route('/')
class EstudianteList(Resource):
    @estudiante_ns.marshal_list_with(estudiante_model)
    def get(self):
        """Listar todos los estudiantes"""
        return listar_estudiantes()

    @estudiante_ns.expect(estudiante_model, validate=True)
    @estudiante_ns.marshal_with(estudiante_model, code=201)
    def post(self):
        """Crear un nuevo estudiante"""
        data = estudiante_ns.payload
        new_id = crear_estudiante(data['nombre'], data['email'], data['edad'])
        return obtener_estudiante_por_id(new_id), 201

@estudiante_ns.route('/<int:id>')
@estudiante_ns.param('id', 'ID del estudiante')
class Estudiante(Resource):
    @estudiante_ns.marshal_with(estudiante_model)
    def get(self, id):
        """Obtener un estudiante por ID"""
        estudiante = obtener_estudiante_por_id(id)
        if not estudiante:
            api.abort(404, "Estudiante no encontrado")
        return estudiante
