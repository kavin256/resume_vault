<template>
  <div class="home-view">
    <div class="page-header">
      <h1>Vault</h1>
      <p class="page-description">
        Welcome — manage your master profile and generate tailored resumes.
      </p>
    </div>
  
    <!-- Summary stats -->
    <div class="stats-grid">
      <div class="stat-card card">
        <div class="stat-value">12</div>
        <div class="stat-label">Resumes Generated</div>
      </div>

      <div class="stat-card card">
        <div class="stat-value">9</div>
        <div class="stat-label">Applications Submitted</div>
      </div>

      <div class="stat-card card">
        <div class="stat-value">3</div>
        <div class="stat-label">Saved Profiles</div>
      </div>
    </div>

    <!-- Recent application history -->
    <div class="card applications-card">
      <h2 class="section-title">Recent Applications</h2>
      <div class="applications-list">
        <div class="app-row">
          <div class="app-company">TechCorp Inc.</div>
          <div class="app-role">Senior Full-Stack Engineer</div>
          <div class="app-date">2025-12-15</div>
          <button class="btn-details" @click="openDrawer(applications[0])">Details</button>
        </div>

        <div class="app-row">
          <div class="app-company">InnovateLab</div>
          <div class="app-role">Frontend Engineer</div>
          <div class="app-date">2025-11-28</div>
          <button class="btn-details" @click="openDrawer(applications[1])">Details</button>
        </div>

        <div class="app-row">
          <div class="app-company">StartupCo</div>
          <div class="app-role">Backend Engineer</div>
          <div class="app-date">2025-10-05</div>
          <button class="btn-details" @click="openDrawer(applications[2])">Details</button>
        </div>
      </div>
    </div>

    <!-- Drawer overlay -->
    <div v-if="drawerOpen" class="drawer-overlay" @click="closeDrawer"></div>

    <!-- Drawer -->
    <div class="drawer" :class="{ 'drawer-open': drawerOpen }">
      <div class="drawer-header">
        <h3>Application Details</h3>
        <button class="drawer-close" @click="closeDrawer">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div class="drawer-content" v-if="selectedApp">
        <!-- Job Details -->
        <div class="drawer-section">
          <h4 class="drawer-section-title">Job Details</h4>
          <div class="detail-row">
            <span class="detail-label">Company</span>
            <span class="detail-value">{{ selectedApp.company }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Position</span>
            <span class="detail-value">{{ selectedApp.position }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Job ID</span>
            <span class="detail-value">{{ selectedApp.jobId }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Posting Link</span>
            <a :href="selectedApp.postingLink" target="_blank" class="detail-link">View Posting →</a>
          </div>
        </div>

        <!-- Job Description -->
        <div class="drawer-section">
          <h4 class="drawer-section-title">Job Description</h4>
          <div class="job-description">{{ selectedApp.jobDescription }}</div>
        </div>

        <!-- Date Generated -->
        <div class="drawer-section">
          <h4 class="drawer-section-title">Generation Info</h4>
          <div class="detail-row">
            <span class="detail-label">Date Generated</span>
            <span class="detail-value">{{ selectedApp.dateGenerated }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const drawerOpen = ref(false)
const selectedApp = ref(null)

// Dummy application data
const applications = [
  {
    company: 'TechCorp Inc.',
    position: 'Senior Full-Stack Engineer',
    jobId: 'REQ-2024-SE-4567',
    postingLink: 'https://techcorp.com/careers/senior-fullstack-engineer-4567',
    jobDescription: `We are seeking an experienced Senior Full-Stack Software Engineer to join our growing engineering team. You will be responsible for designing, developing, and maintaining scalable web applications that serve millions of users worldwide.

Key Responsibilities:
• Design and implement robust, scalable backend services
• Build responsive, performant frontend applications
• Collaborate with product managers and designers
• Write clean, maintainable code with comprehensive test coverage
• Participate in code reviews and mentor junior engineers

Required Qualifications:
• 5+ years of professional software development experience
• Strong proficiency in JavaScript/TypeScript and Python
• Experience with modern frontend frameworks (React, Vue.js, or Angular)
• Solid understanding of backend technologies (Node.js, FastAPI, Django)`,
    dateGenerated: '2025-12-15'
  },
  {
    company: 'InnovateLab',
    position: 'Frontend Engineer',
    jobId: 'JOB-2024-FE-123',
    postingLink: 'https://innovatelab.com/careers/frontend-engineer',
    jobDescription: `Join our frontend team to build beautiful, responsive user interfaces using modern web technologies. You'll work closely with designers to bring creative visions to life.

Requirements:
• 3+ years of frontend development experience
• Expert knowledge of React or Vue.js
• Strong CSS and responsive design skills
• Experience with state management libraries`,
    dateGenerated: '2025-11-28'
  },
  {
    company: 'StartupCo',
    position: 'Backend Engineer',
    jobId: 'HIRE-2024-BE-789',
    postingLink: 'https://startupco.com/jobs/backend-engineer',
    jobDescription: `We're looking for a talented backend engineer to help us scale our infrastructure and build robust APIs. You'll be working on challenging problems in distributed systems.

What you'll do:
• Design and build scalable microservices
• Optimize database performance
• Implement secure authentication and authorization
• Deploy and monitor production systems`,
    dateGenerated: '2025-10-05'
  }
]

function openDrawer(app) {
  selectedApp.value = app
  drawerOpen.value = true
  document.body.style.overflow = 'hidden'
}

function closeDrawer() {
  drawerOpen.value = false
  document.body.style.overflow = ''
}
</script>

<style scoped>
.home-view {
  width: 100%;
  max-width: none;
  margin: 0 auto;
  padding: 40px 48px 64px 48px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}

.page-description {
  font-size: 16px;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

/* Stats grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 18px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

/* Applications list */
.applications-card { padding: 18px; }
.applications-list { display: flex; flex-direction: column; gap: 10px; }
.app-row { display: grid; grid-template-columns: 1.6fr 2fr 1fr auto; gap: 12px; align-items: center; padding: 10px 8px; border-radius: 8px; }
.app-row:nth-child(odd) { background: #fbfdff; }
.app-company { font-weight: 600; color: #0f172a; }
.app-role { color: #334155; font-size: 14px; }
.app-date { color: #64748b; font-size: 13px; }

.btn-details {
  padding: 6px 16px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-details:hover {
  background: #e2e8f0;
  border-color: #94a3b8;
  color: #334155;
}

/* Drawer overlay */
.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 200;
  backdrop-filter: blur(2px);
}

/* Drawer */
.drawer {
  position: fixed;
  right: -500px;
  top: 0;
  width: 500px;
  height: 100vh;
  background: #ffffff;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15);
  z-index: 201;
  transition: right 0.3s ease;
  overflow-y: auto;
}

.drawer.drawer-open {
  right: 0;
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  background: #ffffff;
  z-index: 1;
}

.drawer-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.drawer-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}

.drawer-close:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.drawer-content {
  padding: 28px;
}

.drawer-section {
  margin-bottom: 32px;
}

.drawer-section:last-child {
  margin-bottom: 0;
}

.drawer-section-title {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 16px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  flex-shrink: 0;
  width: 120px;
}

.detail-value {
  font-size: 14px;
  color: #0f172a;
  text-align: right;
  flex: 1;
}

.detail-link {
  font-size: 14px;
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.15s ease;
}

.detail-link:hover {
  color: #2563eb;
  text-decoration: underline;
}

.job-description {
  font-size: 14px;
  color: #334155;
  line-height: 1.7;
  white-space: pre-line;
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

/* Mobile drawer - slide from bottom */
@media (max-width: 768px) {
  .drawer {
    right: auto;
    bottom: -100%;
    left: 0;
    top: auto;
    width: 100%;
    height: 80vh;
    border-radius: 16px 16px 0 0;
    transition: bottom 0.3s ease;
  }

  .drawer.drawer-open {
    right: auto;
    bottom: 0;
  }
}

@media (max-width: 900px) {
  .stats-grid { grid-template-columns: 1fr; }
  .app-row { grid-template-columns: 1fr; gap: 8px; }
  .app-date, .btn-details { justify-self: start; }
}
</style>
