CREATE DATABASE IF NOT EXISTS appclassroom;
USE appclassroom;

-- Tabla de roles (coincide con models/rol.py)
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_identificacion VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    rol_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    nivel_educativo ENUM('Primaria', 'Secundaria', 'Universidad', 'Posgrado', 'Otro') NOT NULL,
    institucion_educativa VARCHAR(100),
    carrera_area_estudio VARCHAR(100),
    fecha_ingreso DATE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS profesores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    especialidad VARCHAR(100) NOT NULL,
    titulo_academico VARCHAR(100),
    anos_experiencia INT,
    departamento VARCHAR(100),
    fecha_contratacion DATE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
-- Tabla de materias (coincide con models/materia.py)
CREATE TABLE IF NOT EXISTS materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    codigo VARCHAR(20) UNIQUE,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de profesores por materia (relación muchos a muchos)
CREATE TABLE IF NOT EXISTS materia_profesores (
    materia_id INT NOT NULL,
    profesor_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (materia_id, profesor_id),
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
    FOREIGN KEY (profesor_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de inscripciones (coincide con models/inscripcion.py)
CREATE TABLE IF NOT EXISTS inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    materia_id INT NOT NULL,
    estado ENUM('activo', 'completado', 'retirado') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id),
    UNIQUE (estudiante_id, materia_id)
);

-- Tabla de tipos de tarea (coincide con models/tipo_tarea.py)
CREATE TABLE IF NOT EXISTS tipos_tarea (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de tareas (coincide con models/tarea.py)
CREATE TABLE IF NOT EXISTS tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    materia_id INT NOT NULL,
    tipo_tarea_id INT,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_entrega DATETIME NOT NULL,
    puntos_posibles DECIMAL(5,2) DEFAULT 100.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
    FOREIGN KEY (tipo_tarea_id) REFERENCES tipos_tarea(id)
);

-- Tabla de entregas (coincide con models/entrega.py)
CREATE TABLE IF NOT EXISTS entregas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tarea_id INT NOT NULL,
    estudiante_id INT NOT NULL,
    archivo_url VARCHAR(255),
    comentario TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tarea_id) REFERENCES tareas(id) ON DELETE CASCADE,
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE (tarea_id, estudiante_id)
);

-- Tabla de calificaciones (coincide con models/calificacion.py)
CREATE TABLE IF NOT EXISTS calificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entrega_id INT NOT NULL,
    profesor_id INT NOT NULL,
    puntuacion DECIMAL(5,2) NOT NULL,
    comentario TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (entrega_id) REFERENCES entregas(id) ON DELETE CASCADE,
    FOREIGN KEY (profesor_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE (entrega_id)
);

-- Datos iniciales para pruebas
INSERT INTO roles (nombre, descripcion) VALUES
('admin', 'Administrador del sistema'),
('profesor', 'Usuario con privilegios de enseñanza'),
('estudiante', 'Usuario que puede tomar materias');

INSERT INTO usuarios (username, email, password_hash, nombre, apellido) VALUES
('admin1', 'admin@escuela.com', '$2b$12$...', 'Admin', 'Principal'),
('profe1', 'profesor@escuela.com', '$2b$12$...', 'Juan', 'Pérez'),
('est1', 'estudiante1@escuela.com', '$2b$12$...', 'Ana', 'García'),
('est2', 'estudiante2@escuela.com', '$2b$12$...', 'Carlos', 'López');


INSERT INTO materias (nombre, descripcion, codigo) VALUES
('Matemáticas Avanzadas', 'Álgebra lineal y cálculo', 'MATH-301'),
('Programación Python', 'Fundamentos de Python', 'PROG-101');

INSERT INTO materia_profesores (materia_id, profesor_id) VALUES
(1, 2), (2, 2);

INSERT INTO inscripciones (estudiante_id, materia_id) VALUES
(3, 1), (4, 1), (3, 2);

INSERT INTO tipos_tarea (nombre, descripcion) VALUES
('Tarea', 'Ejercicios prácticos'),
('Proyecto', 'Trabajo de investigación'),
('Examen', 'Evaluación de conocimientos');

INSERT INTO tareas (materia_id, tipo_tarea_id, titulo, descripcion, fecha_entrega) VALUES
(1, 1, 'Tarea 1', 'Resolver problemas de álgebra', DATE_ADD(NOW(), INTERVAL 7 DAY)),
(2, 2, 'Proyecto Final', 'Desarrollar una aplicación', DATE_ADD(NOW(), INTERVAL 14 DAY));