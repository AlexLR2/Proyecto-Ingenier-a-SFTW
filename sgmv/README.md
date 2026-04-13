# 🚗 SGMV — Sistema de Gestión de Mantenimiento Vehicular

> **Dirigido a:** Personal técnico que desee implementar o desplegar el sistema.

---

## 📐 Especificaciones Técnicas

### Stack tecnológico

| Capa | Tecnología | Versión mínima requerida |
|------|-----------|--------------------------|
| Backend | Python | **3.8+** |
| Framework web | Flask | **2.0+** |
| Base de datos (desarrollo) | SQLite | Incluido en Python stdlib |
| Base de datos (producción) | MySQL | **8.0+** |
| Frontend | HTML5 / CSS3 / JavaScript | ES6+ (Chrome 80+, Edge 80+) |

### Dependencias Python

```
flask==2.3.x  (o superior compatible)
```

Archivo `requirements.txt`:
```
flask>=2.0.0
```

Para MySQL en producción, agregar:
```
flask>=2.0.0
pymysql>=1.0.0
```

---

## ⚙️ Instalación y puesta en marcha

### Requisitos previos

- **Python 3.8 o superior** — https://www.python.org/downloads/
  - Marcar ✅ **"Add Python to PATH"** durante la instalación
- **pip** — incluido con Python 3.4+
- **Navegador:** Chrome 80+ o Edge 80+

### Verificar instalación de Python

```bash
python --version      # Debe mostrar Python 3.8+
pip --version         # Debe mostrar pip 20+
```

### Paso 1 — Descomprimir el proyecto

```
sgmv_app/
├── backend/
│   ├── app.py              ← Servidor API REST
│   └── sgmv_database.sql   ← Script SQL para MySQL
└── frontend/
    ├── index.html
    ├── dashboard.html
    ├── vehiculos.html
    ├── mantenimientos.html
    ├── alertas.html
    ├── historial.html
    ├── css/styles.css
    └── js/api.js
```

### Paso 2 — Instalar Flask

```bash
pip install flask
```

O usando el módulo Python directamente:

```bash
python -m pip install flask
```

### Paso 3 — Iniciar el servidor

```bash
cd sgmv_app/backend
python app.py
```

Salida esperada:
```
✅ BD inicializada
🚗 SGMV API corriendo en http://localhost:5000
 * Running on http://127.0.0.1:5000
```

### Paso 4 — Abrir la aplicación

```
http://localhost:5000
```

**La terminal/cmd debe permanecer abierta** mientras se usa la aplicación.

---

## 🗄️ Base de datos

### Modo desarrollo — SQLite (por defecto)

El archivo `sgmv.db` se crea automáticamente en `backend/` al primer arranque. Contiene los datos del SQL original ya cargados. No requiere configuración.

Para inspeccionar la BD en SQLite:
```bash
# Instalar SQLite browser: https://sqlitebrowser.org/
# O usar línea de comandos:
sqlite3 backend/sgmv.db
sqlite> SELECT * FROM vehiculos;
sqlite> .quit
```

### Modo producción — MySQL 8.0

**1.** Cargar el esquema:
```bash
mysql -u root -p < backend/sgmv_database.sql
```

**2.** Modificar `backend/app.py` — reemplazar la función `get_db()`:

```python
import pymysql

DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'tu_password',
    'database': 'sgmv',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)
```

**3.** Instalar el conector MySQL:
```bash
pip install pymysql
```

---

## 🔌 API REST — Referencia de endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/login` | Autenticar usuario |
| `GET` | `/api/usuarios` | Listar usuarios |
| `GET` | `/api/vehiculos` | Listar vehículos (opcional: `?id_usuario=N`) |
| `POST` | `/api/vehiculos` | Crear vehículo |
| `PUT` | `/api/vehiculos/:id` | Actualizar vehículo |
| `DELETE` | `/api/vehiculos/:id` | Eliminar vehículo |
| `GET` | `/api/mantenimientos` | Listar mantenimientos (opcional: `?id_vehiculo=N`) |
| `POST` | `/api/mantenimientos` | Crear mantenimiento |
| `PUT` | `/api/mantenimientos/:id` | Actualizar mantenimiento |
| `DELETE` | `/api/mantenimientos/:id` | Eliminar mantenimiento |
| `GET` | `/api/alertas` | Listar alertas |
| `POST` | `/api/alertas` | Crear alerta |
| `PUT` | `/api/alertas/:id` | Actualizar estado de alerta |
| `DELETE` | `/api/alertas/:id` | Eliminar alerta |
| `GET` | `/api/tipos` | Listar tipos de mantenimiento |
| `GET` | `/api/dashboard` | Estadísticas generales |

Todos los endpoints devuelven **JSON** y soportan **CORS**.

---

## 🔧 Configuración de puertos

Por defecto el servidor corre en el puerto **5000**. Para cambiarlo:

```python
# En app.py, última línea:
app.run(debug=True, port=8080)  # Cambiar 5000 por el puerto deseado
```

Y actualizar en `frontend/js/api.js`:
```javascript
const API_URL = 'http://localhost:8080/api'; // Actualizar puerto
```

---

## 🐛 Solución de problemas comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `pip no se reconoce` | Python no está en PATH | Reinstalar Python marcando "Add to PATH" |
| `invalid syntax` al escribir pip | Estás dentro del intérprete Python (`>>>`) | Escribe `exit()` primero |
| `Address already in use` | Puerto 5000 ocupado | Cambiar puerto en `app.py` |
| `Module not found: flask` | Flask no instalado | Ejecutar `pip install flask` |
| Página en blanco | Backend no está corriendo | Ejecutar `python app.py` primero |
| `BD conectada` no aparece en verde | Backend detenido | Reiniciar `python app.py` |

---

*Ingeniería de Software · 2026*
