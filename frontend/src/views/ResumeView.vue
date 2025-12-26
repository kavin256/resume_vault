<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useResumeStore } from '../stores/resume'
import type { Resume } from '../types'

const route = useRoute()
const router = useRouter()
const resumeStore = useResumeStore()

const resumeId = ref(parseInt(route.params.id as string))
const relatedResumes = ref<Resume[]>([])
const showAlert = ref(false)
const alertMessage = ref('')
const alertType = ref<'success' | 'error'>('success')

onMounted(async () => {
  try {
    await resumeStore.fetchResume(resumeId.value)
    if (resumeStore.currentResume) {
      loadRelatedResumes(resumeStore.currentResume.company_id)
    }
  } catch (error) {
    displayAlert('Failed to load resume', 'error')
  }
})

async function loadRelatedResumes(companyId: number) {
  try {
    const resumes = await resumeStore.fetchResumesByCompany(companyId)
    relatedResumes.value = resumes.filter((r) => r.id !== resumeId.value)
  } catch (error) {
    console.error('Failed to load related resumes:', error)
  }
}

async function copyToClipboard() {
  if (!resumeStore.currentResume) return

  try {
    await navigator.clipboard.writeText(resumeStore.currentResume.resume_content)
    displayAlert('Resume copied to clipboard!', 'success')
  } catch (error) {
    displayAlert('Failed to copy to clipboard', 'error')
  }
}

function printResume() {
  window.print()
}

function renderMarkdown(content: string): string {
  return content
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
}

function formatDate(dateString: string | undefined): string {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

function displayAlert(message: string, type: 'success' | 'error') {
  alertMessage.value = message
  alertType.value = type
  showAlert.value = true
  setTimeout(() => {
    showAlert.value = false
  }, 5000)
}
</script>

<template>
  <div v-if="showAlert" :class="`alert alert-${alertType}`">
    {{ alertMessage }}
  </div>

  <div v-if="resumeStore.loading" style="text-align: center; padding: 4rem">
    <p style="color: var(--text-secondary)">Loading resume...</p>
  </div>

  <div v-else-if="!resumeStore.currentResume" style="text-align: center; padding: 4rem">
    <p style="color: var(--danger-color)">Resume not found</p>
    <router-link to="/companies" class="btn btn-primary" style="margin-top: 1rem">Back to Companies</router-link>
  </div>

  <div v-else>
    <div class="card">
      <div class="card-header">
        <div>
          <h2 class="card-title">{{ resumeStore.currentResume.resume_title || 'Tailored Resume' }}</h2>
          <p style="color: var(--text-secondary); margin-top: 0.5rem">
            Company ID: {{ resumeStore.currentResume.company_id }}
          </p>
        </div>
        <div style="display: flex; gap: 0.5rem">
          <button class="btn btn-sm btn-secondary" @click="copyToClipboard">Copy Text</button>
          <button class="btn btn-sm btn-outline" @click="printResume">Print</button>
          <router-link to="/companies" class="btn btn-sm btn-outline">Back to Companies</router-link>
        </div>
      </div>

      <div style="padding: 1rem; background: var(--bg-color); border-radius: 6px; margin-bottom: 1rem">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem">
          <div>
            <strong>Version:</strong> {{ resumeStore.currentResume.resume_version }}
          </div>
          <div>
            <strong>Generated:</strong> {{ formatDate(resumeStore.currentResume.created_at) }}
          </div>
          <div>
            <strong>Model:</strong> {{ resumeStore.currentResume.ai_model_used || 'N/A' }}
          </div>
          <div>
            <strong>Status:</strong>
            <span v-if="resumeStore.currentResume.is_sent" class="badge badge-applied">Sent</span>
            <span v-else class="badge badge-not-applied">Draft</span>
          </div>
        </div>

        <div v-if="resumeStore.currentResume.keywords_targeted" style="margin-top: 1rem">
          <strong>Keywords Targeted:</strong> {{ resumeStore.currentResume.keywords_targeted }}
        </div>
      </div>

      <div class="resume-content" v-html="renderMarkdown(resumeStore.currentResume.resume_content)"></div>
    </div>

    <div v-if="relatedResumes.length > 0" class="card">
      <div class="card-header">
        <h3 class="card-title">Related Resumes</h3>
      </div>
      <div v-for="resume in relatedResumes" :key="resume.id" style="padding: 1rem; background: var(--bg-color); border-radius: 6px; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center">
        <div>
          <strong>{{ resume.resume_title || 'Resume ' + resume.resume_version }}</strong>
          <div style="color: var(--text-secondary); font-size: 0.875rem">
            Created: {{ formatDate(resume.created_at) }}
            <span v-if="resume.is_sent" class="badge badge-applied" style="margin-left: 0.5rem">Sent</span>
          </div>
        </div>
        <router-link :to="`/resume/${resume.id}`" class="btn btn-sm btn-outline">View</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media print {
  .card-header,
  .btn,
  button,
  a.btn {
    display: none !important;
  }

  .card {
    box-shadow: none;
    padding: 0;
  }

  .resume-content {
    box-shadow: none;
  }
}
</style>
