"""
SGMV — Backend API REST
Flask + SQLite (desarrollo) / MySQL (producción)
Ejecutar: python app.py
Puerto:   http://localhost:5000
"""

from flask import Flask, jsonify, request, send_from_directory
import sqlite3, os, json
from datetime import date

app = Flask(__name__)

# ── CONFIG ──────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), 'sgmv.db')
FRONTEND = os.path.join(os.path.dirname(__file__), '..', 'frontend')

# ── CORS manual ─────────────────────────────────────────────────
@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin']  = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(FRONTEND, path)):
        return send_from_directory(FRONTEND, path)
    return send_from_directory(FRONTEND, 'index.html')

# ── DB HELPER ────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def rows_to_list(rows):
    return [dict(r) for r in rows]

# ── INIT DB (crea tablas + seed con datos del SQL original) ──────
def init_db():
    if os.path.exists(DB_PATH):
        return
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre     VARCHAR(100),
        email      VARCHAR(100) UNIQUE,
        password   VARCHAR(100)
    );

    CREATE TABLE IF NOT EXISTS vehiculos (
        id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
        placa       VARCHAR(10) UNIQUE,
        marca       VARCHAR(50),
        modelo      VARCHAR(50),
        anio        INTEGER,
        id_usuario  INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
    );

    CREATE TABLE IF NOT EXISTS tipos_mantenimiento (
        id_tipo     INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre      VARCHAR(100),
        descripcion VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS mantenimientos (
        id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_vehiculo      INTEGER,
        id_tipo          INTEGER,
        fecha            DATE,
        kilometraje      INTEGER,
        costo            DECIMAL(10,2),
        descripcion      VARCHAR(255),
        FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
        FOREIGN KEY (id_tipo)     REFERENCES tipos_mantenimiento(id_tipo)
    );

    CREATE TABLE IF NOT EXISTS alertas (
        id_alerta   INTEGER PRIMARY KEY AUTOINCREMENT,
        id_vehiculo INTEGER,
        mensaje     VARCHAR(255),
        fecha       DATE,
        estado      VARCHAR(20) DEFAULT 'pendiente',
        FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo)
    );
    """)

    # Seed — datos exactos del SQL entregado
    c.executemany("INSERT INTO usuarios (nombre,email,password) VALUES (?,?,?)", [
        ('Carlos Perez',  'carlos@mail.com', '1234'),
        ('Ana Torres',    'ana@mail.com',    '1234'),
        ('Luis Gomez',    'luis@mail.com',   '1234'),
        ('Maria Lopez',   'maria@mail.com',  '1234'),
    ])
    c.executemany("INSERT INTO vehiculos (placa,marca,modelo,anio,id_usuario) VALUES (?,?,?,?,?)", [
        ('ABC123','Toyota',    'Corolla', 2018, 1),
        ('DEF456','Chevrolet', 'Spark',   2020, 1),
        ('GHI789','Mazda',     '3',       2019, 2),
        ('JKL321','Renault',   'Logan',   2017, 3),
        ('MNO654','Kia',       'Rio',     2021, 4),
    ])
    c.executemany("INSERT INTO tipos_mantenimiento (nombre,descripcion) VALUES (?,?)", [
        ('Cambio de aceite', 'Cambio aceite motor'),
        ('Frenos',           'Revision frenos'),
        ('Llantas',          'Cambio llantas'),
        ('Bateria',          'Cambio bateria'),
        ('General',          'Revision general'),
    ])
    c.executemany(
        "INSERT INTO mantenimientos (id_vehiculo,id_tipo,fecha,kilometraje,costo,descripcion) VALUES (?,?,?,?,?,?)", [
        (1,1,'2026-01-10',50000,120000,'Cambio aceite'),
        (1,2,'2026-02-15',52000, 80000,'Pastillas freno'),
        (2,1,'2026-01-05',20000,110000,'Aceite'),
        (2,5,'2026-02-20',22000,150000,'Revision'),
        (3,3,'2026-01-18',30000,900000,'Llantas nuevas'),
        (3,1,'2026-02-28',32000,120000,'Aceite'),
        (4,4,'2026-01-22',70000,250000,'Bateria'),
        (4,1,'2026-03-01',72000,120000,'Aceite'),
        (5,5,'2026-02-11',10000,140000,'General'),
        (5,1,'2026-03-05',12000,120000,'Aceite'),
    ])
    c.executemany("INSERT INTO alertas (id_vehiculo,mensaje,fecha,estado) VALUES (?,?,?,?)", [
        (1,'Cambio aceite proximo', '2026-04-01','pendiente'),
        (2,'Revision general',      '2026-04-10','pendiente'),
        (3,'Cambio llantas',        '2026-05-01','pendiente'),
        (4,'Revision frenos',       '2026-04-20','pendiente'),
        (5,'Cambio aceite',         '2026-04-15','pendiente'),
    ])
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada con datos de prueba")

# ════════════════════════════════════════════════════
#  API — USUARIOS  (CRUD completo)
# ════════════════════════════════════════════════════
@app.route('/api/usuarios', methods=['GET','OPTIONS'])
def get_usuarios():
    if request.method == 'OPTIONS': return jsonify({}), 200
    db = get_db()
    rows = db.execute("SELECT id_usuario,nombre,email FROM usuarios ORDER BY id_usuario").fetchall()
    db.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    db = get_db()
    row = db.execute("SELECT id_usuario,nombre,email FROM usuarios WHERE id_usuario=?", (id,)).fetchone()
    db.close()
    return jsonify(dict(row)) if row else (jsonify({'error':'No encontrado'}), 404)

@app.route('/api/usuarios', methods=['POST'])
def create_usuario():
    d = request.get_json()
    if not d or not d.get('nombre') or not d.get('email'):
        return jsonify({'error':'nombre y email son requeridos'}), 400
    db = get_db()
    try:
        cur = db.execute("INSERT INTO usuarios (nombre,email,password) VALUES (?,?,?)",
                         (d['nombre'], d['email'], d.get('password','1234')))
        db.commit()
        new_id = cur.lastrowid
        db.close()
        return jsonify({'id_usuario': new_id, 'mensaje': 'Usuario creado'}), 201
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/usuarios/<int:id>', methods=['PUT','OPTIONS'])
def update_usuario(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    d = request.get_json()
    db = get_db()
    db.execute("UPDATE usuarios SET nombre=?, email=? WHERE id_usuario=?",
               (d.get('nombre'), d.get('email'), id))
    db.commit()
    db.close()
    return jsonify({'mensaje': 'Usuario actualizado'})

@app.route('/api/usuarios/<int:id>', methods=['DELETE','OPTIONS'])
def delete_usuario(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    db = get_db()
    db.execute("DELETE FROM usuarios WHERE id_usuario=?", (id,))
    db.commit()
    db.close()
    return jsonify({'mensaje': 'Usuario eliminado'})

@app.route('/api/login', methods=['POST','OPTIONS'])
def login():
    if request.method == 'OPTIONS': return jsonify({}), 200
    d = request.get_json()
    db = get_db()
    row = db.execute(
        "SELECT id_usuario,nombre,email FROM usuarios WHERE email=? AND password=?",
        (d.get('email',''), d.get('password',''))
    ).fetchone()
    db.close()
    if row:
        return jsonify({'ok': True, 'usuario': dict(row)})
    return jsonify({'ok': False, 'error': 'Credenciales incorrectas'}), 401

# ════════════════════════════════════════════════════
#  API — VEHÍCULOS  (CRUD completo)
# ════════════════════════════════════════════════════
@app.route('/api/vehiculos', methods=['GET','OPTIONS'])
def get_vehiculos():
    if request.method == 'OPTIONS': return jsonify({}), 200
    id_usuario = request.args.get('id_usuario')
    db = get_db()
    if id_usuario:
        rows = db.execute("""
            SELECT v.*, u.nombre as propietario FROM vehiculos v
            JOIN usuarios u ON u.id_usuario = v.id_usuario
            WHERE v.id_usuario=? ORDER BY v.id_vehiculo""", (id_usuario,)).fetchall()
    else:
        rows = db.execute("""
            SELECT v.*, u.nombre as propietario FROM vehiculos v
            JOIN usuarios u ON u.id_usuario = v.id_usuario
            ORDER BY v.id_vehiculo""").fetchall()
    db.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/vehiculos/<int:id>', methods=['GET'])
def get_vehiculo(id):
    db = get_db()
    row = db.execute("""
        SELECT v.*, u.nombre as propietario FROM vehiculos v
        JOIN usuarios u ON u.id_usuario = v.id_usuario
        WHERE v.id_vehiculo=?""", (id,)).fetchone()
    db.close()
    return jsonify(dict(row)) if row else (jsonify({'error':'No encontrado'}), 404)

@app.route('/api/vehiculos', methods=['POST'])
def create_vehiculo():
    d = request.get_json()
    if not d or not d.get('placa'):
        return jsonify({'error':'placa es requerida'}), 400
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO vehiculos (placa,marca,modelo,anio,id_usuario) VALUES (?,?,?,?,?)",
            (d['placa'], d.get('marca',''), d.get('modelo',''), d.get('anio'), d.get('id_usuario')))
        db.commit()
        new_id = cur.lastrowid
        db.close()
        return jsonify({'id_vehiculo': new_id, 'mensaje': 'Vehículo creado'}), 201
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/vehiculos/<int:id>', methods=['PUT','OPTIONS'])
def update_vehiculo(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    d = request.get_json()
    db = get_db()
    db.execute("""UPDATE vehiculos SET placa=?,marca=?,modelo=?,anio=?,id_usuario=?
                  WHERE id_vehiculo=?""",
               (d.get('placa'), d.get('marca'), d.get('modelo'),
                d.get('anio'), d.get('id_usuario'), id))
    db.commit()
    db.close()
    return jsonify({'mensaje': 'Vehículo actualizado'})

@app.route('/api/vehiculos/<int:id>', methods=['DELETE','OPTIONS'])
def delete_vehiculo(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    db = get_db()
    db.execute("DELETE FROM mantenimientos WHERE id_vehiculo=?", (id,))
    db.execute("DELETE FROM alertas WHERE id_vehiculo=?", (id,))
    db.execute("DELETE FROM vehiculos WHERE id_vehiculo=?", (id,))
    db.commit()
    db.close()
    return jsonify({'mensaje': 'Vehículo eliminado'})

# ════════════════════════════════════════════════════
#  API — MANTENIMIENTOS  (CRUD completo)
# ════════════════════════════════════════════════════
@app.route('/api/mantenimientos', methods=['GET','OPTIONS'])
def get_mantenimientos():
    if request.method == 'OPTIONS': return jsonify({}), 200
    id_vehiculo = request.args.get('id_vehiculo')
    db = get_db()
    if id_vehiculo:
        rows = db.execute("""
            SELECT m.*, v.placa, v.marca, v.modelo, t.nombre as tipo_nombre
            FROM mantenimientos m
            JOIN vehiculos v ON v.id_vehiculo = m.id_vehiculo
            JOIN tipos_mantenimiento t ON t.id_tipo = m.id_tipo
            WHERE m.id_vehiculo=? ORDER BY m.fecha DESC""", (id_vehiculo,)).fetchall()
    else:
        rows = db.execute("""
            SELECT m.*, v.placa, v.marca, v.modelo, t.nombre as tipo_nombre
            FROM mantenimientos m
            JOIN vehiculos v ON v.id_vehiculo = m.id_vehiculo
            JOIN tipos_mantenimiento t ON t.id_tipo = m.id_tipo
            ORDER BY m.fecha DESC""").fetchall()
    db.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/mantenimientos', methods=['POST'])
def create_mantenimiento():
    d = request.get_json()
    db = get_db()
    try:
        cur = db.execute("""INSERT INTO mantenimientos
            (id_vehiculo,id_tipo,fecha,kilometraje,costo,descripcion)
            VALUES (?,?,?,?,?,?)""",
            (d['id_vehiculo'], d['id_tipo'], d['fecha'],
             d.get('kilometraje'), d.get('costo'), d.get('descripcion','')))
        db.commit()
        new_id = cur.lastrowid
        db.close()
        return jsonify({'id_mantenimiento': new_id, 'mensaje': 'Mantenimiento registrado'}), 201
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/mantenimientos/<int:id>', methods=['PUT','OPTIONS'])
def update_mantenimiento(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    d = request.get_json()
    db = get_db()
    db.execute("""UPDATE mantenimientos SET id_vehiculo=?,id_tipo=?,fecha=?,
                  kilometraje=?,costo=?,descripcion=? WHERE id_mantenimiento=?""",
               (d.get('id_vehiculo'), d.get('id_tipo'), d.get('fecha'),
                d.get('kilometraje'), d.get('costo'), d.get('descripcion'), id))
    db.commit()
    db.close()
    return jsonify({'mensaje': 'Mantenimiento actualizado'})

@app.route('/api/mantenimientos/<int:id>', methods=['DELETE','OPTIONS'])
def delete_mantenimiento(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    db = get_db()
    db.execute("DELETE FROM mantenimientos WHERE id_mantenimiento=?", (id,))
    db.commit()
    db.close()
    return jsonify({'mensaje': 'Mantenimiento eliminado'})

# ════════════════════════════════════════════════════
#  API — ALERTAS  (CRUD completo)
# ════════════════════════════════════════════════════
@app.route('/api/alertas', methods=['GET','OPTIONS'])
def get_alertas():
    if request.method == 'OPTIONS': return jsonify({}), 200
    db = get_db()
    rows = db.execute("""
        SELECT a.*, v.placa, v.marca, v.modelo FROM alertas a
        JOIN vehiculos v ON v.id_vehiculo = a.id_vehiculo
        ORDER BY a.fecha ASC""").fetchall()
    db.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/alertas', methods=['POST'])
def create_alerta():
    d = request.get_json()
    db = get_db()
    cur = db.execute("INSERT INTO alertas (id_vehiculo,mensaje,fecha,estado) VALUES (?,?,?,?)",
                     (d['id_vehiculo'], d['mensaje'], d['fecha'], d.get('estado','pendiente')))
    db.commit()
    new_id = cur.lastrowid
    db.close()
    return jsonify({'id_alerta': new_id, 'mensaje': 'Alerta creada'}), 201

@app.route('/api/alertas/<int:id>', methods=['PUT','OPTIONS'])
def update_alerta(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    d = request.get_json()
    db = get_db()
    db.execute("UPDATE alertas SET estado=?,mensaje=?,fecha=? WHERE id_alerta=?",
               (d.get('estado'), d.get('mensaje'), d.get('fecha'), id))
    db.commit()
    db.close()
    return jsonify({'mensaje': 'Alerta actualizada'})

@app.route('/api/alertas/<int:id>', methods=['DELETE','OPTIONS'])
def delete_alerta(id):
    if request.method == 'OPTIONS': return jsonify({}), 200
    db = get_db()
    db.execute("DELETE FROM alertas WHERE id_alerta=?", (id,))
    db.commit()
    db.close()
    return jsonify({'mensaje': 'Alerta eliminada'})

# ════════════════════════════════════════════════════
#  API — TIPOS_MANTENIMIENTO  (catálogo)
# ════════════════════════════════════════════════════
@app.route('/api/tipos', methods=['GET','OPTIONS'])
def get_tipos():
    if request.method == 'OPTIONS': return jsonify({}), 200
    db = get_db()
    rows = db.execute("SELECT * FROM tipos_mantenimiento ORDER BY id_tipo").fetchall()
    db.close()
    return jsonify(rows_to_list(rows))

# ════════════════════════════════════════════════════
#  API — DASHBOARD (stats)
# ════════════════════════════════════════════════════
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    db = get_db()
    stats = {
        'total_vehiculos':     db.execute("SELECT COUNT(*) as n FROM vehiculos").fetchone()['n'],
        'total_mantenimientos':db.execute("SELECT COUNT(*) as n FROM mantenimientos").fetchone()['n'],
        'alertas_pendientes':  db.execute("SELECT COUNT(*) as n FROM alertas WHERE estado='pendiente'").fetchone()['n'],
        'total_usuarios':      db.execute("SELECT COUNT(*) as n FROM usuarios").fetchone()['n'],
        'gasto_total':         db.execute("SELECT COALESCE(SUM(costo),0) as s FROM mantenimientos").fetchone()['s'],
        'ultimos_mantenimientos': rows_to_list(db.execute("""
            SELECT m.fecha, m.costo, m.descripcion, v.placa, v.marca, v.modelo, t.nombre as tipo
            FROM mantenimientos m
            JOIN vehiculos v ON v.id_vehiculo = m.id_vehiculo
            JOIN tipos_mantenimiento t ON t.id_tipo = m.id_tipo
            ORDER BY m.fecha DESC LIMIT 5""").fetchall()),
        'alertas_activas': rows_to_list(db.execute("""
            SELECT a.*, v.placa, v.marca, v.modelo FROM alertas a
            JOIN vehiculos v ON v.id_vehiculo = a.id_vehiculo
            WHERE a.estado='pendiente' ORDER BY a.fecha ASC LIMIT 5""").fetchall()),
    }
    db.close()
    return jsonify(stats)

# ── MAIN ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    print("🚗 SGMV API corriendo en http://localhost:5000")
    print("📋 Endpoints: /api/usuarios /api/vehiculos /api/mantenimientos /api/alertas /api/tipos")
    app.run(debug=True, port=5000)
