<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCompanyStore } from '../stores/company'
import { useResumeStore } from '../stores/resume'
import type { Company } from '../types'

const router = useRouter()
const companyStore = useCompanyStore()
const resumeStore = useResumeStore()

const showForm = ref(false)
const showAlert = ref(false)
const alertMessage = ref('')
const alertType = ref<'success' | 'error' | 'info'>('success')

const formData = ref<Company>({
  company_name: '',
  industry: '',
  company_website: '',
  company_description: '',
  job_title: '',
  job_description: '',
  job_requirements: '',
  job_url: '',
  application_status: 'not_applied',
  notes: '',
})

onMounted(async () => {
  await companyStore.fetchCompanies()
})

function toggleForm() {
  showForm.value = !showForm.value
}

function resetForm() {
  formData.value = {
    company_name: '',
    industry: '',
    company_website: '',
    company_description: '',
    job_title: '',
    job_description: '',
    job_requirements: '',
    job_url: '',
    application_status: 'not_applied',
    notes: '',
  }
}

async function saveCompany() {
  try {
    await companyStore.createCompany(formData.value)
    displayAlert('Company added successfully!', 'success')
    resetForm()
    toggleForm()
  } catch (error) {
    displayAlert('Failed to add company. Please try again.', 'error')
  }
}

async function deleteCompany(id: number) {
  if (!confirm('Are you sure you want to delete this company? This will also delete all associated resumes.')) {
    return
  }

  try {
    await companyStore.deleteCompany(id)
    displayAlert('Company deleted successfully', 'success')
  } catch (error) {
    displayAlert('Failed to delete company', 'error')
  }
}

async function tailorResume(companyId: number) {
  if (!confirm('This will generate a tailored resume using the Mock Tailor function. Continue?')) {
    return
  }

  try {
    const resume = await resumeStore.tailorResume({ company_id: companyId })
    displayAlert('Resume tailored successfully!', 'success')
    setTimeout(() => {
      router.push(`/resume/${resume.id}`)
    }, 1000)
  } catch (error) {
    displayAlert('Failed to tailor resume. Make sure you have created a Master Profile first.', 'error')
  }
}

async function viewResumes(companyId: number) {
  try {
    const resumes = await resumeStore.fetchResumesByCompany(companyId)
    if (resumes.length === 0) {
      displayAlert('No resumes generated for this company yet. Click "Tailor Resume" to create one.', 'info')
      return
    }
    router.push(`/resume/${resumes[resumes.length - 1].id}`)
  } catch (error) {
    displayAlert('Failed to fetch resumes', 'error')
  }
}

function formatStatus(status: string) {
  return status
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function displayAlert(message: string, type: 'success' | 'error' | 'info') {
  alertMessage.value = message
  alertType.value = type
  showAlert.value = true
  setTimeout(() => {
    showAlert.value = false
  }, 5000)
}
</script>

<template>
  <div class="page-header">
    <h1>Company Vault</h1>
    <p>Track companies and job opportunities</p>
  </div>

  <div v-if="showAlert" :class="`alert alert-${alertType}`">
    {{ alertMessage }}
  </div>

  <div class="card">
    <div class="card-header">
      <h2 class="card-title">Add New Company</h2>
      <button type="button" class="btn btn-sm btn-outline" @click="toggleForm">
        {{ showForm ? 'Hide Form' : 'Show Form' }}
      </button>
    </div>

    <form v-if="showForm" @submit.prevent="saveCompany">
      <div class="grid grid-2">
        <div class="form-group">
          <label for="company_name">Company Name *</label>
          <input type="text" id="company_name" v-model="formData.company_name" required />
        </div>
        <div class="form-group">
          <label for="industry">Industry</label>
          <input type="text" id="industry" v-model="formData.industry" placeholder="e.g., Technology, Finance, Healthcare" />
        </div>
      </div>

      <div class="grid grid-2">
        <div class="form-group">
          <label for="company_website">Company Website</label>
          <input type="url" id="company_website" v-model="formData.company_website" placeholder="https://..." />
        </div>
        <div class="form-group">
          <label for="job_url">Job Posting URL</label>
          <input type="url" id="job_url" v-model="formData.job_url" placeholder="https://..." />
        </div>
      </div>

      <div class="form-group">
        <label for="company_description">Company Description</label>
        <textarea id="company_description" v-model="formData.company_description" placeholder="Brief description of the company..."></textarea>
      </div>

      <div class="form-group">
        <label for="job_title">Job Title *</label>
        <input type="text" id="job_title" v-model="formData.job_title" required placeholder="e.g., Senior Software Engineer" />
      </div>

      <div class="form-group">
        <label for="job_description">Job Description *</label>
        <textarea id="job_description" v-model="formData.job_description" style="min-height: 200px" required placeholder="Paste the full job description here..."></textarea>
      </div>

      <div class="form-group">
        <label for="job_requirements">Job Requirements</label>
        <textarea id="job_requirements" v-model="formData.job_requirements" placeholder="Specific requirements extracted from the job posting..."></textarea>
      </div>

      <div class="grid grid-2">
        <div class="form-group">
          <label for="application_status">Application Status</label>
          <select id="application_status" v-model="formData.application_status">
            <option value="not_applied">Not Applied</option>
            <option value="applied">Applied</option>
            <option value="interviewing">Interviewing</option>
            <option value="offer">Offer</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>
        <div class="form-group">
          <label for="notes">Notes</label>
          <input type="text" id="notes" v-model="formData.notes" placeholder="Additional notes..." />
        </div>
      </div>

      <div style="display: flex; gap: 1rem">
        <button type="submit" class="btn btn-primary" :disabled="companyStore.loading">Add Company</button>
        <button type="button" class="btn btn-outline" @click="resetForm">Clear</button>
      </div>
    </form>
  </div>

  <div class="card">
    <div class="card-header">
      <h2 class="card-title">Saved Companies</h2>
    </div>

    <div v-if="companyStore.loading" style="text-align: center; padding: 2rem">
      <p style="color: var(--text-secondary)">Loading companies...</p>
    </div>

    <div v-else-if="companyStore.companies.length === 0" style="padding: 2rem">
      <p style="color: var(--text-secondary)">No companies added yet. Add your first company above!</p>
    </div>

    <div v-else>
      <div v-for="company in companyStore.companies" :key="company.id" class="company-card">
        <h3>{{ company.company_name }}</h3>
        <div class="job-title">{{ company.job_title }}</div>

        <div class="meta">
          <span v-if="company.industry">Industry: {{ company.industry }}</span>
          <span :class="`badge badge-${company.application_status}`">
            {{ formatStatus(company.application_status || 'not_applied') }}
          </span>
        </div>

        <div style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.9rem">
          <strong>Job Description:</strong>
          <div style="margin-top: 0.5rem; max-height: 100px; overflow-y: auto; background: var(--bg-color); padding: 0.5rem; border-radius: 4px">
            {{ company.job_description.substring(0, 300) }}{{ company.job_description.length > 300 ? '...' : '' }}
          </div>
        </div>

        <div v-if="company.notes" style="margin-top: 0.5rem; color: var(--text-secondary); font-size: 0.9rem">
          <strong>Notes:</strong> {{ company.notes }}
        </div>

        <div class="actions">
          <button class="btn btn-sm btn-primary" @click="tailorResume(company.id!)" :disabled="resumeStore.loading">
            Tailor Resume
          </button>
          <button class="btn btn-sm btn-secondary" @click="viewResumes(company.id!)">View Resumes</button>
          <a v-if="company.company_website" :href="company.company_website" target="_blank" class="btn btn-sm btn-outline">Website</a>
          <a v-if="company.job_url" :href="company.job_url" target="_blank" class="btn btn-sm btn-outline">Job Posting</a>
          <button class="btn btn-sm btn-danger" @click="deleteCompany(company.id!)">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>
