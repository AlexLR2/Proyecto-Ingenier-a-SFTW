// ── SGMV API Client ─────────────────────────────────────────────
// Todas las llamadas al backend pasan por aquí.
// Cambia BASE_URL si el backend corre en otro puerto.
const API_URL = 'http://localhost:5000/api';

// Usuario en sesión (guardado en sessionStorage)
const Session = {
  get()       { try { return JSON.parse(sessionStorage.getItem('sgmv_user')); } catch{ return null; } },
  set(u)      { sessionStorage.setItem('sgmv_user', JSON.stringify(u)); },
  clear()     { sessionStorage.removeItem('sgmv_user'); },
  require()   {
    const u = this.get();
    if (!u) { window.location.href = 'index.html'; return null; }
    return u;
  }
};

// ── FETCH HELPER ─────────────────────────────────────────────────
async function api(path, opts = {}) {
  const res = await fetch(API_URL + path, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
    body: opts.body ? JSON.stringify(opts.body) : undefined,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Error del servidor');
  return data;
}

const API = {
  // Usuarios
  getUsuarios:    ()       => api('/usuarios'),
  createUsuario:  (d)      => api('/usuarios',      { method:'POST', body:d }),
  updateUsuario:  (id, d)  => api(`/usuarios/${id}`,{ method:'PUT',  body:d }),
  deleteUsuario:  (id)     => api(`/usuarios/${id}`,{ method:'DELETE' }),
  login:          (d)      => api('/login',         { method:'POST', body:d }),

  // Vehículos
  getVehiculos:   (uid)    => api('/vehiculos' + (uid ? `?id_usuario=${uid}` : '')),
  createVehiculo: (d)      => api('/vehiculos',      { method:'POST', body:d }),
  updateVehiculo: (id, d)  => api(`/vehiculos/${id}`,{ method:'PUT',  body:d }),
  deleteVehiculo: (id)     => api(`/vehiculos/${id}`,{ method:'DELETE' }),

  // Mantenimientos
  getMantenimientos: (idV) => api('/mantenimientos' + (idV ? `?id_vehiculo=${idV}` : '')),
  createMant:     (d)      => api('/mantenimientos',         { method:'POST', body:d }),
  updateMant:     (id, d)  => api(`/mantenimientos/${id}`,   { method:'PUT',  body:d }),
  deleteMant:     (id)     => api(`/mantenimientos/${id}`,   { method:'DELETE' }),

  // Alertas
  getAlertas:     ()       => api('/alertas'),
  createAlerta:   (d)      => api('/alertas',       { method:'POST', body:d }),
  updateAlerta:   (id, d)  => api(`/alertas/${id}`, { method:'PUT',  body:d }),
  deleteAlerta:   (id)     => api(`/alertas/${id}`, { method:'DELETE' }),

  // Tipos
  getTipos:       ()       => api('/tipos'),

  // Dashboard
  getDashboard:   ()       => api('/dashboard'),
};

// ── SIDEBAR RENDERER ─────────────────────────────────────────────
const NAV = {
  render(active) {
    const user = Session.get();
    const ini = user ? user.nombre.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase() : '??';
    const links = [
      { id:'dashboard',       icon:'📊', label:'Dashboard',      href:'dashboard.html' },
      { id:'vehiculos',       icon:'🚗', label:'Mis Vehículos',  href:'vehiculos.html' },
      { id:'mantenimientos',  icon:'🔧', label:'Mantenimientos', href:'mantenimientos.html' },
      { id:'alertas',         icon:'🔔', label:'Alertas',        href:'alertas.html' },
      { id:'historial',       icon:'📋', label:'Historial',      href:'historial.html' },
    ];
    const html = `
      <aside class="sidebar">
        <div class="sidebar-logo">
          <div class="logo-icon">🚗</div>
          <div><div class="logo-text">SGMV</div><div class="logo-sub">Gestión Vehicular</div></div>
        </div>
        <div class="sidebar-section">Principal</div>
        ${links.map(l => `
          <a href="${l.href}" class="nav-item ${active===l.id?'active':''}">
            <span class="nav-icon">${l.icon}</span><span>${l.label}</span>
          </a>`).join('')}
        <div class="sidebar-section" style="margin-top:16px">Cuenta</div>
        <a href="index.html" class="nav-item" onclick="Session.clear()">
          <span class="nav-icon">🚪</span><span>Cerrar sesión</span>
        </a>
        <div class="sidebar-bottom">
          <div class="user-pill">
            <div class="user-avatar">${ini}</div>
            <div>
              <div class="user-name">${user?.nombre || 'Usuario'}</div>
              <div class="user-role">Propietario</div>
            </div>
          </div>
        </div>
      </aside>`;
    document.getElementById('nav-container').innerHTML = html;
  }
};

// ── TOAST ────────────────────────────────────────────────────────
function toast(msg, type='success') {
  let t = document.getElementById('_toast');
  if (!t) { t = document.createElement('div'); t.id='_toast'; t.className='toast'; document.body.appendChild(t); }
  t.textContent = type==='success' ? '✅ '+msg : '❌ '+msg;
  t.className = `toast ${type} show`;
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 3000);
}

// ── MODAL HELPERS ─────────────────────────────────────────────────
function openModal(id)  { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

// ── SEMAPHORE helper ──────────────────────────────────────────────
function semaphoreHTML(status) {
  return `<div class="semaphore-wrap">
    <div class="semaphore-light s-red   ${status==='red'  ?'active':''}"></div>
    <div class="semaphore-light s-amber ${status==='amber'?'active':''}"></div>
    <div class="semaphore-light s-green ${status==='green'?'active':''}"></div>
  </div>`;
}
function alertStatus(fecha) {
  const diff = (new Date(fecha) - new Date()) / 86400000;
  if (diff < 0)  return 'red';
  if (diff < 15) return 'amber';
  return 'green';
}

// ── FORMAT HELPERS ────────────────────────────────────────────────
const fmt = {
  money: v => v != null ? '$' + Number(v).toLocaleString('es-CO') : '—',
  date:  v => v ? new Date(v+'T00:00:00').toLocaleDateString('es-CO') : '—',
  km:    v => v != null ? Number(v).toLocaleString() + ' km' : '—',
};

// ── API STATUS CHECK ─────────────────────────────────────────────
async function checkApiStatus() {
  const el = document.getElementById('api-status-dot');
  const lbl = document.getElementById('api-status-label');
  if (!el) return;
  try {
    await fetch(API_URL + '/tipos');
    el.className = 'api-dot';
    if (lbl) lbl.textContent = 'BD conectada';
  } catch {
    el.className = 'api-dot offline';
    if (lbl) lbl.textContent = 'Sin conexión';
  }
}
