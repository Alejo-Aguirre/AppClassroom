from mysql.connector import Error
import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

class UsuarioModel:
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
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios ORDER BY nombre ASC")
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetch_by_id(self, id):
        if not self.connection or not self.connection.is_connected():
            return None
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def login(self, username, password_hash):
        if not self.connection or not self.connection.is_connected():
            return None
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT id, username, rol_id, activo FROM usuarios WHERE username = %s AND password_hash = %s"
        cursor.execute(sql, (username, password_hash))
        result = cursor.fetchone()
        cursor.close()
        return result

    def delete(self, id):
        if not self.connection or not self.connection.is_connected():
            return False
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
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
                id,
                numero_identificacion,
                nombre,
                apellido,
                email,
                telefono,
                username,
                password_hash,
                activo,
                rol_id,
                created_at,
                updated_at
            FROM usuarios
            WHERE username = %s
        """

        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def obtener_por_id(self, id):
        return self.fetch_by_id(id)


# Funciones de ayuda (helpers)
def obtener_usuario_por_username(username):
    model = UsuarioModel()
    return model.obtener_por_username(username)

def obtener_usuario_por_id(id):
    model = UsuarioModel()
    return model.obtener_por_id(id)