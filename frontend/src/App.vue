<template>
  <div id="app">
    <AppNav />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import AppNav from './components/AppNav.vue'

// Shared state - provided to all views
const masterProfile = ref({
  name: '',
  email: '',
  phone: '',
  professionalExperience: '',
  skills: '',
  education: '',
  licenses: '',
  summary: ''
})

provide('masterProfile', masterProfile)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #f8f9fb;
  color: #1a202c;
  display: block !important;
  place-items: unset !important;
}

#app {
  min-height: 100vh;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
  text-align: left !important;
  display: flex;
  width: 100vw;
  overflow-x: hidden;
}

.main-content {
  flex: 1;
  margin-left: 260px;
  min-height: 100vh;
  background: #f8f9fb;
  overflow-x: hidden;
}

/* Mobile responsive */
@media (max-width: 768px) {
  #app {
    flex-direction: column;
  }

  .main-content {
    margin-left: 0;
    margin-top: 72px;
  }
}
</style>
