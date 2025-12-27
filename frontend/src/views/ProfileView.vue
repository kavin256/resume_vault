<template>
  <div class="profile-view">
    <div class="page-header">
      <h1>Master Profile</h1>
      <p class="page-description">Enter your career information once. This data will be used to generate tailored resumes.</p>
    </div>

    <div class="card">
      <h2 class="section-title">Personal Information</h2>

      <div class="form-row">
        <div class="form-group">
          <label>Full Name <span class="required">*</span></label>
          <input v-model="profile.name" type="text" required />
        </div>

        <div class="form-group">
          <label>Email <span class="required">*</span></label>
          <input v-model="profile.email" type="email" required />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Phone <span class="required">*</span></label>
          <input v-model="profile.phone" type="tel" required />
        </div>
      </div>
    </div>

    <div class="card">
      <h2 class="section-title">Professional Summary</h2>

      <div class="form-group">
        <label>Summary <span class="required">*</span></label>
        <textarea v-model="profile.summary" rows="3" required placeholder="e.g., Results-driven software engineer with 5+ years of experience building scalable web applications..."></textarea>
      </div>
    </div>

    <div class="card">
      <h2 class="section-title">Professional Experience</h2>

      <div class="form-group">
        <label>Work Experience <span class="required">*</span></label>
        <textarea v-model="profile.professionalExperience" rows="10" required placeholder="List your professional experience in detail. Include company names, job titles, dates, and key accomplishments.

Example:
Senior Software Engineer | Tech Company Inc. | 2020 - Present
• Led development of customer-facing web application serving 100k+ users
• Improved application performance by 40% through optimization initiatives
• Mentored team of 3 junior developers

Software Engineer | StartupCo | 2018 - 2020
• Built REST APIs using Python and FastAPI
• Implemented CI/CD pipeline reducing deployment time by 60%"></textarea>
      </div>
    </div>

    <div class="card">
      <h2 class="section-title">Skills & Education</h2>

      <div class="form-group">
        <label>Technical Skills <span class="required">*</span></label>
        <textarea v-model="profile.skills" rows="3" required placeholder="e.g., JavaScript, TypeScript, Python, React, Vue.js, Node.js, FastAPI, PostgreSQL, MongoDB, AWS, Docker, Git"></textarea>
      </div>

      <div class="form-group">
        <label>Education <span class="required">*</span></label>
        <input v-model="profile.education" type="text" required placeholder="e.g., BS Computer Science, Stanford University, 2018" />
      </div>

      <div class="form-group">
        <label>Licenses & Certifications</label>
        <textarea v-model="profile.licenses" rows="2" placeholder="e.g., AWS Certified Solutions Architect, PMP Certification, Certified Kubernetes Administrator"></textarea>
      </div>
    </div>

    <div class="action-footer">
      <!-- TODO: Remove this test button before production -->
      <button @click="toggleTestData" class="btn btn-secondary">
        {{ hasData ? 'Clear Data' : 'Fill with Test Data' }}
      </button>
      <button
        @click="continueToGenerate"
        :disabled="!isFormValid"
        class="btn btn-primary"
        :class="{ 'btn-disabled': !isFormValid }"
      >
        Continue to Generate Resume →
      </button>
    </div>
  </div>
</template>

<script setup>
import { inject, computed } from 'vue'
import { useRouter } from 'vue-router'

const profile = inject('masterProfile')
const router = useRouter()

// Validate all required fields are filled
const isFormValid = computed(() => {
  return profile.value.name?.trim() &&
         profile.value.email?.trim() &&
         profile.value.phone?.trim() &&
         profile.value.summary?.trim() &&
         profile.value.professionalExperience?.trim() &&
         profile.value.skills?.trim() &&
         profile.value.education?.trim()
})

// TODO: Remove this computed and function before production
const hasData = computed(() => {
  return profile.value.name || profile.value.email || profile.value.phone ||
         profile.value.summary || profile.value.professionalExperience ||
         profile.value.skills || profile.value.education || profile.value.licenses
})

function continueToGenerate() {
  if (isFormValid.value) {
    router.push('/generate')
  }
}

// TODO: Remove this test function before production
function toggleTestData() {
  if (hasData.value) {
    // Clear data
    profile.value.name = ''
    profile.value.email = ''
    profile.value.phone = ''
    profile.value.summary = ''
    profile.value.professionalExperience = ''
    profile.value.skills = ''
    profile.value.education = ''
    profile.value.licenses = ''
  } else {
    // Fill with test data
    profile.value.name = 'Sarah Chen'
    profile.value.email = 'sarah.chen@email.com'
    profile.value.phone = '+1 (555) 123-4567'
    profile.value.summary = 'Results-driven Full-Stack Software Engineer with 5+ years of experience building scalable web applications and backend systems. Proven track record of leading development teams, optimizing performance, and delivering high-quality solutions that serve 100k+ users. Strong expertise in modern JavaScript frameworks, Python, and cloud technologies.'
    profile.value.professionalExperience = `Senior Full-Stack Software Engineer | TechCorp Inc. | 2021 - Present
• Led development of customer-facing SaaS platform serving 150k+ active users
• Architected and implemented microservices backend using FastAPI and PostgreSQL
• Improved application performance by 45% through code optimization and caching strategies
• Mentored team of 4 junior developers and conducted regular code reviews
• Implemented CI/CD pipeline using GitHub Actions, reducing deployment time by 70%

Full-Stack Software Engineer | InnovateLab | 2019 - 2021
• Built responsive web applications using React and Vue.js
• Developed RESTful APIs and GraphQL endpoints for mobile and web clients
• Integrated third-party services including Stripe, Twilio, and SendGrid
• Collaborated with product team to define features and technical requirements
• Reduced bug count by 60% through comprehensive unit and integration testing

Junior Software Developer | StartupCo | 2018 - 2019
• Contributed to full-stack development using Node.js and MongoDB
• Implemented user authentication and authorization features
• Participated in agile development process with 2-week sprints`
    profile.value.skills = 'JavaScript, TypeScript, Python, React, Vue.js, Node.js, Express, FastAPI, Django, PostgreSQL, MongoDB, Redis, AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes, Git, GitHub Actions, CI/CD, REST APIs, GraphQL, WebSockets, Jest, Pytest, Agile/Scrum'
    profile.value.education = 'BS Computer Science, Stanford University, 2018'
    profile.value.licenses = 'AWS Certified Solutions Architect - Associate, MongoDB Certified Developer'
  }
}
</script>

<style scoped>
.profile-view {
  max-width: 1000px;
  margin: 0 auto;
  padding: 48px 32px 64px;
}

.page-header {
  margin-bottom: 40px;
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

.card {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.section-title {
  font-size: 19px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 24px 0;
  letter-spacing: -0.01em;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group:last-child {
  margin-bottom: 0;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 14px;
  color: #334155;
}

.required {
  color: #dc2626;
}

input,
textarea {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-family: inherit;
  font-size: 15px;
  font-weight: 400;
  color: #0f172a;
  background: #ffffff;
  line-height: 1.5;
  transition: border-color 0.15s ease;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #3b82f6;
  background: #ffffff;
}

input::placeholder,
textarea::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.action-footer {
  margin-top: 32px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  display: inline-block;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled,
.btn-primary.btn-disabled {
  background: #94a3b8;
  color: #cbd5e1;
  cursor: not-allowed;
  opacity: 0.6;
}

/* TODO: Remove this style before production */
.btn-secondary {
  background: #e2e8f0;
  color: #475569;
}

.btn-secondary:hover {
  background: #cbd5e1;
}
</style>
