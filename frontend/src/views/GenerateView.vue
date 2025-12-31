<template>
  <div class="generate-view">
    <div class="page-header">
      <h1>Generate Resume</h1>
      <p class="page-description">Paste the job description below and generate a tailored resume.</p>
    </div>

    <div class="card">
      <h2 class="section-title">Job Details</h2>

      <div class="form-row">
        <div class="form-group">
          <label>Company Name <span class="required">*</span></label>
          <input v-model="companyName" type="text" required placeholder="e.g., Google, Microsoft, Amazon" />
        </div>

        <div class="form-group">
          <label>Position <span class="required">*</span></label>
          <input v-model="position" type="text" required placeholder="e.g., Senior Software Engineer" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Job ID</label>
          <input v-model="jobId" type="text" placeholder="e.g., REQ-2024-12345 (optional)" />
        </div>

        <div class="form-group">
          <label>Posting Link</label>
          <input v-model="postingLink" type="url" placeholder="e.g., https://company.com/careers/job-12345 (optional)" />
        </div>
      </div>
    </div>

    <div class="card">
      <h2 class="section-title">Job Description</h2>
      <textarea
        v-model="jobDescription"
        rows="12"
        placeholder="Paste the full job description here..."
        required
      ></textarea>
      <!-- TODO: Remove this test button before production -->
      <div class="jd-actions">
        <Button @click="toggleTestJD" variant="outline">
          {{ jobDescription ? 'Clear JD' : 'Fill with Test JD' }}
        </Button>
      </div>
    </div>

    <div class="generate-section">
      <Button @click="handleGenerate" :disabled="isGenerating" size="lg">
        {{ isGenerating ? 'Generating...' : 'Generate Resume & Cover Letter' }}
      </Button>
    </div>

    <div v-if="error" class="error-card">
      <strong>Error:</strong> {{ error }}
    </div>

    <div v-if="generated" class="download-card">
      <div class="download-header">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 11l3 3L22 4"></path>
          <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"></path>
        </svg>
        <h3>Documents Ready</h3>
      </div>
      <p class="download-description">Your resume and cover letter have been generated successfully.</p>

      <div class="ats-scores">
        <div class="ats-score-item">
          <div class="ats-score-label">Resume ATS Score</div>
          <div class="ats-score-value" :class="getScoreClass(resumeAtsScore)">
            {{ resumeAtsScore }}%
          </div>
        </div>
        <div class="ats-score-item">
          <div class="ats-score-label">Cover Letter ATS Score</div>
          <div class="ats-score-value" :class="getScoreClass(coverLetterAtsScore)">
            {{ coverLetterAtsScore }}%
          </div>
        </div>
      </div>

      <div class="download-buttons">
        <Button @click="downloadResume" variant="secondary" class="flex-1 button-with-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"></path>
          </svg>
          Download Resume
        </Button>
        <Button @click="downloadCoverLetter" variant="secondary" class="flex-1 button-with-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"></path>
          </svg>
          Download Cover Letter
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@clerk/vue'
import { Button } from '@/components/ui/button'

const auth = useAuth()
const jobDescription = ref('')
const companyName = ref('')
const position = ref('')
const jobId = ref('')
const postingLink = ref('')
const isGenerating = ref(false)
const generated = ref(false)
const resumeBase64 = ref('')
const coverLetterBase64 = ref('')
const resumeAtsScore = ref(0)
const coverLetterAtsScore = ref(0)
const error = ref('')

async function handleGenerate() {
  error.value = ''
  isGenerating.value = true
  generated.value = false

  try {
    // Get authentication token
    const token = await auth.getToken.value()
    if (!token) {
      throw new Error('No authentication token. Please sign in.')
    }

    // Backend now fetches master profile from database using authenticated user
    const API_URL = import.meta.env.VITE_API_URL || 'https://resume-vault.fly.dev'
    const response = await fetch(`${API_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        job_description: jobDescription.value,
        company_name: companyName.value,
        position: position.value,
        job_id: jobId.value,
        posting_link: postingLink.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Generation failed')
    }

    const data = await response.json()
    resumeBase64.value = data.resume_base64
    coverLetterBase64.value = data.cover_letter_base64
    resumeAtsScore.value = data.resume_ats_score
    coverLetterAtsScore.value = data.cover_letter_ats_score
    generated.value = true
  } catch (err) {
    error.value = err.message || 'Failed to generate documents. Make sure the backend is running.'
    console.error(err)
  } finally {
    isGenerating.value = false
  }
}

// TODO: Remove this test function before production
function toggleTestJD() {
  if (jobDescription.value) {
    // Clear all fields
    jobDescription.value = ''
    companyName.value = ''
    position.value = ''
    jobId.value = ''
    postingLink.value = ''
  } else {
    // Fill with test data
    companyName.value = 'TechCorp Inc.'
    position.value = 'Senior Full-Stack Software Engineer'
    jobId.value = 'REQ-2024-SE-4567'
    postingLink.value = 'https://techcorp.com/careers/senior-fullstack-engineer-4567'
    jobDescription.value = `Senior Full-Stack Software Engineer

About the Role:
We are seeking an experienced Senior Full-Stack Software Engineer to join our growing engineering team. You will be responsible for designing, developing, and maintaining scalable web applications that serve millions of users worldwide.

Key Responsibilities:
• Design and implement robust, scalable backend services using modern frameworks
• Build responsive, performant frontend applications with modern JavaScript frameworks
• Collaborate with product managers and designers to define and implement new features
• Write clean, maintainable code with comprehensive test coverage
• Participate in code reviews and mentor junior engineers
• Optimize application performance and scalability
• Deploy and maintain applications in cloud environments

Required Qualifications:
• 5+ years of professional software development experience
• Strong proficiency in JavaScript/TypeScript and Python
• Experience with modern frontend frameworks (React, Vue.js, or Angular)
• Solid understanding of backend technologies (Node.js, FastAPI, Django, or similar)
• Experience with relational databases (PostgreSQL, MySQL) and NoSQL databases (MongoDB, Redis)
• Proficiency with Git and version control workflows
• Experience with cloud platforms (AWS, GCP, or Azure)
• Strong understanding of RESTful API design and GraphQL
• Experience with containerization (Docker) and orchestration (Kubernetes)

Preferred Qualifications:
• Experience with CI/CD pipelines and DevOps practices
• Knowledge of microservices architecture
• Experience with WebSockets and real-time applications
• Contributions to open-source projects
• Bachelor's degree in Computer Science or related field

What We Offer:
• Competitive salary and equity package
• Comprehensive health, dental, and vision insurance
• Flexible work arrangements (remote-friendly)
• Professional development budget
• Collaborative and innovative work environment`
  }
}

function getScoreClass(score) {
  if (score >= 85) return 'score-excellent'
  if (score >= 70) return 'score-good'
  if (score >= 60) return 'score-fair'
  return 'score-poor'
}

function downloadResume() {
  downloadFile(resumeBase64.value, 'resume.pdf', 'application/pdf')
}

function downloadCoverLetter() {
  downloadFile(coverLetterBase64.value, 'cover_letter.pdf', 'application/pdf')
}

function downloadFile(base64Data, filename, mimeType) {
  const binaryString = atob(base64Data)
  const bytes = new Uint8Array(binaryString.length)
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i)
  }

  const blob = new Blob([bytes], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.generate-view {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 48px 64px 48px;
}

@media (max-width: 1024px) {
  .generate-view {
    padding: 32px 32px 64px 32px;
  }
}

@media (max-width: 768px) {
  .generate-view {
    padding: 24px 20px 48px 20px;
  }
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.page-description {
  font-size: 15px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.card {
  width: 100%;
  background: #ffffff;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  padding: 28px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  margin-bottom: 20px;
}

.section-title {
  font-size: 17px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 18px 0;
  letter-spacing: -0.01em;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

label {
  display: block;
  margin-bottom: 7px;
  font-weight: 500;
  font-size: 13px;
  color: #334155;
}

.required {
  color: #dc2626;
}

input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 400;
  color: #0f172a;
  background: #ffffff;
  line-height: 1.5;
  transition: border-color 0.15s ease;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  background: #ffffff;
}

input::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
  font-size: 13px;
  font-weight: 400;
  color: #0f172a;
  background: #ffffff;
  line-height: 1.6;
  resize: vertical;
  transition: border-color 0.15s ease;
}

textarea:focus {
  outline: none;
  border-color: #3b82f6;
  background: #ffffff;
}

textarea::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

/* TODO: Remove this style before production */
.jd-actions {
  margin-top: 12px;
  text-align: left;
}

.generate-section {
  margin-top: 20px;
  text-align: center;
}


.error-card {
  margin-top: 24px;
  padding: 20px 24px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #991b1b;
  font-size: 15px;
  line-height: 1.6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.error-card strong {
  font-weight: 600;
}

.download-card {
  margin-top: 32px;
  background: #f0fdf4;
  border-radius: 12px;
  border: 1px solid #86efac;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.download-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 10px;
}

.download-header svg {
  color: #16a34a;
  flex-shrink: 0;
}

.download-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
  letter-spacing: -0.01em;
}

.download-description {
  font-size: 15px;
  color: #64748b;
  margin: 0 0 20px 0;
  line-height: 1.5;
}

.ats-scores {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.ats-score-item {
  flex: 1;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.ats-score-label {
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.ats-score-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.02em;
}

.score-excellent {
  color: #16a34a;
}

.score-good {
  color: #2563eb;
}

.score-fair {
  color: #ea580c;
}

.score-poor {
  color: #dc2626;
}

@media (max-width: 640px) {
  .ats-scores {
    flex-direction: column;
    gap: 12px;
  }
}

.download-buttons {
  display: flex;
  gap: 12px;
}

.flex-1 {
  flex: 1;
}

.button-with-icon {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 640px) {
  .download-buttons {
    flex-direction: column;
  }
}
</style>
