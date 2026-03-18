# 🚗 SGMV — Sistema de Gestión de Mantenimiento Vehicular

> Aplicación web para el registro, seguimiento y control del mantenimiento preventivo y correctivo de vehículos. Pensada para propietarios individuales, familias y pequeñas flotas.

---

## 📋 Descripción

**SGMV** es una aplicación frontend que centraliza toda la información de mantenimiento vehicular en un solo lugar. Permite registrar servicios, consultar historiales, y recibir alertas visuales tipo **semáforo** (🔴🟡🟢) antes de que un mantenimiento se venza.

### ¿Qué hace el sistema?

| Módulo | Funcionalidad |
|---|---|
| 🔐 Login | Autenticación con usuario y contraseña |
| 📊 Dashboard | Vista general con alertas activas y estado de la flota |
| 🚗 Vehículos | Registro, edición y eliminación de vehículos |
| 🔧 Mantenimientos | Formulario de registro de servicios realizados |
| 🔔 Alertas | Sistema semáforo de mantenimientos próximos o vencidos |
| 📋 Historial | Listado completo con filtros por vehículo, tipo y fecha |

### ¿Qué NO hace (en esta fase)?

- No integra con talleres, aseguradoras ni entidades gubernamentales
- No tiene módulo de análisis financiero avanzado
- No ofrece aplicación móvil nativa (es responsive web)
- No incluye inteligencia artificial ni automatización avanzada

---

## 🖼️ Capturas de pantalla

### Login
![Login](screenshots/login.png)

### Dashboard — Vista general
![Dashboard](screenshots/dashboard.png)

### Mis Vehículos
![Vehículos](screenshots/vehiculos.png)

### Registrar Mantenimiento
![Mantenimiento](screenshots/mantenimientos.png)

### Alertas — Sistema semáforo
![Alertas](screenshots/alertas.png)

### Historial con filtros
![Historial](screenshots/historial.png)

---

## 🗂️ Estructura del proyecto

```
sgmv/
├── login.html                  # Pantalla de inicio de sesión
├── css/
│   └── styles.css              # Sistema de diseño y estilos globales
├── js/
│   └── nav.js                  # Componente de navegación compartido
└── pages/
    ├── dashboard.html          # Panel principal con resumen
    ├── vehiculos.html          # Gestión de vehículos
    ├── mantenimientos.html     # Registro de mantenimientos
    ├── alertas.html            # Sistema de alertas semáforo
    └── historial.html          # Historial completo con filtros
```

---

## ⚙️ Cómo correr el proyecto

### Opción 1 — Abrir directamente (sin servidor)

1. **Clona o descarga** el repositorio:

```bash
git clone https://github.com/tu-usuario/sgmv.git
cd sgmv
```

2. **Abre el archivo de entrada** en tu navegador:

```bash
# En Windows
start login.html

# En macOS
open login.html

# En Linux
xdg-open login.html
```

3. **Inicia sesión** con las credenciales de prueba:
   - Usuario: `admin`
   - Contraseña: `1234`

> ✅ **No requiere instalación de dependencias**. Es HTML/CSS/JS puro, funciona directamente en el navegador.

---

### Opción 2 — Con servidor local (recomendado para evitar errores CORS)

#### Usando Python

```bash
# Python 3
cd sgmv
python -m http.server 8080

# Luego abre en el navegador:
# http://localhost:8080/login.html
```

#### Usando Node.js con `serve`

```bash
# Instalar serve globalmente (solo una vez)
npm install -g serve

# Ejecutar en la carpeta del proyecto
cd sgmv
serve .

# Luego abre:
# http://localhost:3000/login.html
```

#### Usando VS Code — Live Server

1. Instala la extensión **Live Server** en VS Code
2. Abre el archivo `login.html`
3. Haz clic derecho → **Open with Live Server**
4. El navegador abrirá automáticamente `http://127.0.0.1:5500/login.html`

---

## 🧭 Navegación del sistema

```
login.html
    └── pages/dashboard.html      ← Inicio tras iniciar sesión
            ├── vehiculos.html    ← Gestión de vehículos
            ├── mantenimientos.html ← Registrar servicios
            ├── alertas.html      ← Alertas y semáforo
            └── historial.html    ← Historial completo
```

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| **HTML5** | Estructura de vistas y formularios |
| **CSS3** | Sistema de diseño, variables, animaciones |
| **JavaScript (ES6+)** | Lógica de UI, filtros, formularios, navegación |
| **Google Fonts** | Tipografías: Syne (display) + DM Sans (body) |

> **Sin frameworks, sin dependencias externas.** Todo funciona con tecnologías web estándar.

---

## 📐 Requerimientos funcionales implementados

| RF | Descripción | Vista |
|---|---|---|
| RF-001 | Registrar mantenimiento con tipo, fecha, km y costo | `mantenimientos.html` |
| RF-002 | Consultar historial con filtros | `historial.html` |
| RF-003 | Alertas semáforo verde/amarillo/rojo | `alertas.html` |
| RF-004 | Registrar/editar/eliminar vehículos | `vehiculos.html` |
| RF-005 | Autenticación con usuario y contraseña | `login.html` |

---

## 👥 Usuarios del sistema

| Rol | Acceso |
|---|---|
| **Administrador** | CRUD completo: vehículos, mantenimientos, alertas |
| **Usuario Familiar** | Solo consulta y registro de mantenimientos |

---

## 📄 Licencia

Proyecto académico — Ingeniería de Software · 2025.

---

## 🤝 Autor

Desarrollado como parte del proyecto SGMV para la asignatura de Ingeniería de Software.