import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

class EstudianteModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", 3306),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
        except Error as e:
            print("Error al conectar a la base de datos:", e)
            self.connection = None
    
    def fetch_all(self):
        if not self.connection or not self.connection.is_connected():
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = """
                SELECT 
                    e.id AS estudiante_id,
                    u.id AS usuario_id,
                    u.numero_identificacion,
                    u.nombre,
                    u.apellido,
                    u.email,
                    u.telefono,
                    u.username,
                    u.activo,
                    u.rol_id,
                    u.created_at,
                    u.updated_at,
                    e.nivel_educativo,
                    e.institucion_educativa,
                    e.carrera_area_estudio,
                    e.fecha_ingreso
                FROM estudiantes e
                INNER JOIN usuarios u ON e.usuario_id = u.id
                ORDER BY u.nombre ASC
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    
    def fetch_by_id(self, id):
        if not self.connection or not self.connection.is_connected():
            return None

        cursor = self.connection.cursor(dictionary=True)

        sql = """
            SELECT 
                e.id AS estudiante_id,
                u.id AS usuario_id,
                u.numero_identificacion,
                u.nombre,
                u.apellido,
                u.email,
                u.telefono,
                u.username,
                u.activo,
                u.rol_id,
                u.created_at,
                u.updated_at,
                e.nivel_educativo,
                e.institucion_educativa,
                e.carrera_area_estudio,
                e.fecha_ingreso
            FROM estudiantes e
            INNER JOIN usuarios u ON e.usuario_id = u.id
            WHERE e.id = %s
        """

        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result


    def create(self, numero_identificacion, nombre, apellido, email, telefono,
            username, password_hash, activo, rol_id,
            created_at, updated_at,
            nivel_educativo, institucion_educativa,
            carrera_area_estudio, fecha_ingreso):
        
        if not self.connection or not self.connection.is_connected():
            return None

        try:
            cursor = self.connection.cursor()

            # 1. Insertar en la tabla usuarios
            sql_usuario = """
                INSERT INTO usuarios (
                    numero_identificacion, nombre, apellido, email, telefono,
                    username, password_hash, activo, rol_id, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_usuario, (
                numero_identificacion, nombre, apellido, email, telefono,
                username, password_hash, activo, rol_id, created_at, updated_at
            ))

            usuario_id = cursor.lastrowid

            # 2. Insertar en la tabla estudiantes
            sql_estudiante = """
                INSERT INTO estudiantes (
                    usuario_id, nivel_educativo, institucion_educativa,
                    carrera_area_estudio, fecha_ingreso
                ) VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_estudiante, (
                usuario_id, nivel_educativo, institucion_educativa,
                carrera_area_estudio, fecha_ingreso
            ))

            self.connection.commit()
            return usuario_id

        except Exception as e:
            self.connection.rollback()
            print("Error al crear estudiante:", e)
            return None

        finally:
            cursor.close()


    def update(self, id, nombre, email, edad):
        if not self.connection or not self.connection.is_connected():
            return False
        cursor = self.connection.cursor()
        sql = "UPDATE estudiantes SET nombre = %s, email = %s, edad = %s WHERE id = %s"
        cursor.execute(sql, (nombre, email, edad, id))
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0

    def delete(self, estudiante_id):
        if not self.connection or not self.connection.is_connected():
            return False
        
        cursor = self.connection.cursor()
        
        # Primero obtengo el usuario_id del estudiante para eliminar el usuario correcto
        sql_get_usuario = "SELECT usuario_id FROM estudiantes WHERE id = %s"
        cursor.execute(sql_get_usuario, (estudiante_id,))
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            return False  # No existe el estudiante
        
        usuario_id = result[0]
        
        # Elimino el usuario, lo que eliminará el estudiante por ON DELETE CASCADE
        sql_delete_usuario = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql_delete_usuario, (usuario_id,))
        self.connection.commit()
        
        affected = cursor.rowcount
        cursor.close()
        
        return affected > 0


    #organizarlo
    def search(self, termino):
        if not self.connection or not self.connection.is_connected():
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = """
                SELECT 
                    e.id AS estudiante_id,
                    u.id AS usuario_id,
                    u.numero_identificacion,
                    u.nombre,
                    u.apellido,
                    u.email,
                    u.telefono,
                    u.username,
                    u.activo,
                    u.rol_id,
                    u.created_at,
                    u.updated_at,
                    e.nivel_educativo,
                    e.institucion_educativa,
                    e.carrera_area_estudio,
                    e.fecha_ingreso
                FROM estudiantes e
                INNER JOIN usuarios u ON e.usuario_id = u.id
                WHERE u.nombre LIKE %s OR u.apellido LIKE %s OR u.email LIKE %s OR u.numero_identificacion LIKE %s
            """
            like_term = f"%{termino}%"
            cursor.execute(sql, (like_term, like_term, like_term, like_term))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error al buscar estudiantes:", e)
            return []
        finally:
            if cursor:
                cursor.close()
                
                
    def obtener_por_usuario_id(self, usuario_id):
            if not self.connection or not self.connection.is_connected():
                return None

            try:
                cursor = self.connection.cursor(dictionary=True)
                sql = """
                    SELECT 
                        e.id AS estudiante_id,
                        e.usuario_id,
                        e.nivel_educativo,
                        e.institucion_educativa,
                        e.carrera_area_estudio,
                        e.fecha_ingreso
                    FROM estudiantes e
                    WHERE e.usuario_id = %s
                """
                cursor.execute(sql, (usuario_id,))
                result = cursor.fetchone()
                return result
            except Exception as e:
                print("Error al obtener estudiante por usuario_id:", e)
                return None
            finally:
                if cursor:
                    cursor.close()


    def login(self, username, password_hash):
        if not self.connection or not self.connection.is_connected():
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = """
                SELECT id, username, rol_id, activo 
                FROM usuarios 
                WHERE username = %s AND password_hash = %s
            """
            cursor.execute(sql, (username, password_hash))
            result = cursor.fetchone()
            return result
        except Exception as e:
            print("Error al intentar iniciar sesión:", e)
            return None
        finally:
            cursor.close()
