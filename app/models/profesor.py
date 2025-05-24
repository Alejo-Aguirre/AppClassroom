from mysql.connector import Error

import mysql.connector

class ProfesorModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='appclassroom',
                user='root',
                password='root'
            )
        except Error as e:
            print("Error al conectar a la base de datos:", e)
            self.connection = None

    def fetch_all(self):
        if not self.connection or not self.connection.is_connected():
            return []

        cursor = self.connection.cursor(dictionary=True)
        sql = """
            SELECT 
                p.id AS profesor_id,
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
                p.area_especializacion,
                p.titulo_profesional
            FROM profesores p
            INNER JOIN usuarios u ON p.usuario_id = u.id
            ORDER BY u.nombre ASC
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetch_by_id(self, id):
        if not self.connection or not self.connection.is_connected():
            return None
        cursor = self.connection.cursor(dictionary=True)
        sql = """
            SELECT 
                p.id AS profesor_id,
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
                p.area_especializacion,
                p.titulo_profesional
            FROM profesores p
            INNER JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.id = %s
        """
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def create(self, numero_identificacion, nombre, apellido, email, telefono,
               username, password_hash, activo, rol_id, created_at, updated_at,
               area_especializacion, titulo_profesional):
        if not self.connection or not self.connection.is_connected():
            return None
        cursor = self.connection.cursor()

        # Insertar usuario
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

        # Insertar profesor
        sql_profesor = """
            INSERT INTO profesores (
                usuario_id, area_especializacion, titulo_profesional
            ) VALUES (%s, %s, %s)
        """
        cursor.execute(sql_profesor, (usuario_id, area_especializacion, titulo_profesional))

        self.connection.commit()
        cursor.close()
        return usuario_id

    def delete(self, profesor_id):
        if not self.connection or not self.connection.is_connected():
            return False

        cursor = self.connection.cursor()
        sql_get_usuario = "SELECT usuario_id FROM profesores WHERE id = %s"
        cursor.execute(sql_get_usuario, (profesor_id,))
        result = cursor.fetchone()

        if not result:
            cursor.close()
            return False

        usuario_id = result[0]

        sql_delete_usuario = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql_delete_usuario, (usuario_id,))
        self.connection.commit()

        affected = cursor.rowcount
        cursor.close()
        return affected > 0

    def obtener_por_username(self, username):
        if not self.connection or not self.connection.is_connected():
            return None

        cursor = self.connection.cursor(dictionary=True)

        sql = """
            SELECT 
                p.id AS profesor_id,
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
                p.titulo_profesional,
                p.area_expertise,
                p.experiencia_anios
            FROM profesores p
            INNER JOIN usuarios u ON p.usuario_id = u.id
            WHERE u.username = %s
        """

        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result
