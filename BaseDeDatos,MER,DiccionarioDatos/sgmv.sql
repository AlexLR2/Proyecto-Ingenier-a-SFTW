
CREATE DATABASE IF NOT EXISTS sgmv;
USE sgmv;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE vehiculos (
    id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    anio INT,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE tipos_mantenimiento (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(255)
);

CREATE TABLE mantenimientos (
    id_mantenimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT,
    id_tipo INT,
    fecha DATE,
    kilometraje INT,
    costo DECIMAL(10,2),
    descripcion VARCHAR(255),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
    FOREIGN KEY (id_tipo) REFERENCES tipos_mantenimiento(id_tipo)
);

CREATE TABLE alertas (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT,
    mensaje VARCHAR(255),
    fecha DATE,
    estado VARCHAR(20),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo)
);

INSERT INTO usuarios (nombre,email,password) VALUES
('Carlos Perez','carlos@mail.com','1234'),
('Ana Torres','ana@mail.com','1234'),
('Luis Gomez','luis@mail.com','1234'),
('Maria Lopez','maria@mail.com','1234');

INSERT INTO vehiculos (placa,marca,modelo,anio,id_usuario) VALUES
('ABC123','Toyota','Corolla',2018,1),
('DEF456','Chevrolet','Spark',2020,1),
('GHI789','Mazda','3',2019,2),
('JKL321','Renault','Logan',2017,3),
('MNO654','Kia','Rio',2021,4);

INSERT INTO tipos_mantenimiento (nombre,descripcion) VALUES
('Cambio de aceite','Cambio aceite motor'),
('Frenos','Revision frenos'),
('Llantas','Cambio llantas'),
('Bateria','Cambio bateria'),
('General','Revision general');

INSERT INTO mantenimientos (id_vehiculo,id_tipo,fecha,kilometraje,costo,descripcion) VALUES
(1,1,'2026-01-10',50000,120000,'Cambio aceite'),
(1,2,'2026-02-15',52000,80000,'Pastillas freno'),
(2,1,'2026-01-05',20000,110000,'Aceite'),
(2,5,'2026-02-20',22000,150000,'Revision'),
(3,3,'2026-01-18',30000,900000,'Llantas nuevas'),
(3,1,'2026-02-28',32000,120000,'Aceite'),
(4,4,'2026-01-22',70000,250000,'Bateria'),
(4,1,'2026-03-01',72000,120000,'Aceite'),
(5,5,'2026-02-11',10000,140000,'General'),
(5,1,'2026-03-05',12000,120000,'Aceite');

INSERT INTO alertas (id_vehiculo,mensaje,fecha,estado) VALUES
(1,'Cambio aceite proximo','2026-04-01','pendiente'),
(2,'Revision general','2026-04-10','pendiente'),
(3,'Cambio llantas','2026-05-01','pendiente'),
(4,'Revision frenos','2026-04-20','pendiente'),
(5,'Cambio aceite','2026-04-15','pendiente');
