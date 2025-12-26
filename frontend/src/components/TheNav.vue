<template>
  <nav>
    <div class="container">
      <router-link to="/" class="logo">Resume Vault</router-link>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/profile">Master Profile</router-link></li>
        <li><router-link to="/companies">Company Vault</router-link></li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
nav {
  background-color: var(--card-bg);
  box-shadow: var(--shadow);
  padding: 1rem 0;
  margin-bottom: 2rem;
}

nav .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav .logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
}

nav ul {
  list-style: none;
  display: flex;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

nav a {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

nav a:hover,
nav a.router-link-active {
  color: var(--primary-color);
}
</style>
