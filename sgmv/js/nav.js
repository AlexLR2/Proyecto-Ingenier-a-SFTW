// SGMV — Shared Navigation Component
const SGMV = {
  renderSidebar(activePage) {
    const nav = [
      { icon: '📊', label: 'Dashboard',     href: '../index.html',            id: 'dashboard' },
      { icon: '🚗', label: 'Mis Vehículos', href: 'vehiculos.html',           id: 'vehiculos' },
      { icon: '🔧', label: 'Mantenimientos',href: 'mantenimientos.html',       id: 'mantenimientos', badge: '2', badgeClass: 'red' },
      { icon: '🔔', label: 'Alertas',       href: 'alertas.html',             id: 'alertas', badge: '3', badgeClass: 'red' },
      { icon: '📋', label: 'Historial',     href: 'historial.html',           id: 'historial' },
    ];

    return `
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">🚗</div>
        <div>
          <div class="logo-text">SGMV</div>
          <div class="logo-sub">Gestión Vehicular</div>
        </div>
      </div>

      <div class="sidebar-section">Principal</div>
      ${nav.map(n => `
        <a href="${n.href}" class="nav-item ${activePage === n.id ? 'active' : ''}">
          <span class="nav-icon">${n.icon}</span>
          <span>${n.label}</span>
          ${n.badge ? `<span class="nav-badge ${n.badgeClass || ''}">${n.badge}</span>` : ''}
        </a>
      `).join('')}

      <div class="sidebar-section" style="margin-top:16px">Cuenta</div>
      <a href="perfil.html" class="nav-item ${activePage === 'perfil' ? 'active' : ''}">
        <span class="nav-icon">⚙️</span><span>Configuración</span>
      </a>
      <a href="../login.html" class="nav-item">
        <span class="nav-icon">🚪</span><span>Cerrar sesión</span>
      </a>

      <div class="sidebar-bottom">
        <div class="user-pill">
          <div class="user-avatar">CM</div>
          <div>
            <div class="user-name">Carlos M.</div>
            <div class="user-role">Administrador</div>
          </div>
        </div>
      </div>
    </aside>`;
  }
};
