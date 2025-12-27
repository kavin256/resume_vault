<template>
  <nav class="app-nav">
    <div class="nav-container">
      <div class="nav-brand">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
        <span class="brand-text">Resume Vault</span>
      </div>

      <div class="nav-links">
        <router-link to="/profile" class="nav-link">
          Master Profile
        </router-link>
        <router-link to="/generate" class="nav-link">
          Generate Resume
        </router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.app-nav {
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #0f172a;
}

.nav-brand svg {
  flex-shrink: 0;
  color: #3b82f6;
}

.brand-text {
  font-size: 19px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.nav-links {
  display: flex;
  gap: 4px;
}

.nav-link {
  padding: 10px 20px;
  font-size: 15px;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.15s ease;
}

.nav-link:hover {
  color: #0f172a;
  background: #f8fafc;
}

.nav-link.router-link-active {
  color: #3b82f6;
  background: #eff6ff;
}
</style>
