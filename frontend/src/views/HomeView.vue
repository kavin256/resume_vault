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
          <div class="app-status status-interview">Interview</div>
        </div>

        <div class="app-row">
          <div class="app-company">InnovateLab</div>
          <div class="app-role">Frontend Engineer</div>
          <div class="app-date">2025-11-28</div>
          <div class="app-status status-applied">Applied</div>
        </div>

        <div class="app-row">
          <div class="app-company">StartupCo</div>
          <div class="app-role">Backend Engineer</div>
          <div class="app-date">2025-10-05</div>
          <div class="app-status status-rejected">Rejected</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Placeholder Home view — will expand later
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
.app-row { display: grid; grid-template-columns: 1.6fr 2fr 1fr 1fr; gap: 12px; align-items: center; padding: 10px 8px; border-radius: 8px; }
.app-row:nth-child(odd) { background: #fbfdff; }
.app-company { font-weight: 600; color: #0f172a; }
.app-role { color: #334155; font-size: 14px; }
.app-date { color: #64748b; font-size: 13px; }
.app-status { font-weight: 600; padding: 6px 10px; border-radius: 999px; text-align: center; font-size: 13px; }
.status-interview { background: #ecfdf5; color: #166534; border: 1px solid #bbf7d0; }
.status-applied { background: #eff6ff; color: #0369a1; border: 1px solid #bfdbfe; }
.status-rejected { background: #fff7f7; color: #991b1b; border: 1px solid #fecaca; }

@media (max-width: 900px) {
  .stats-grid { grid-template-columns: 1fr; }
  .app-row { grid-template-columns: 1fr; gap: 8px; }
  .app-date, .app-status { justify-self: start; }
}
</style>
