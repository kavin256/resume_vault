<template>
  <div class="edit-form-container">
    <div v-if="isLoading" class="loading-state">
      <p>Loading content...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <Button @click="handleCancel" variant="outline">Go Back</Button>
    </div>

    <div v-else-if="editableContent" class="edit-layout">
      <!-- Left Panel: Edit Form -->
      <div class="edit-panel">
        <div class="panel-header">
          <h4 class="panel-title">Edit Content</h4>
          <div class="panel-actions">
            <Button @click="handleCancel" variant="outline" size="sm" :disabled="isRegenerating">
              Cancel
            </Button>
            <Button @click="handleCompile" variant="default" size="sm" :disabled="isRegenerating">
              {{ isRegenerating ? 'Compiling...' : 'Compile Preview' }}
            </Button>
          </div>
        </div>

        <div class="edit-form">
          <!-- Professional Summary -->
          <div class="form-section">
            <label class="section-label">Professional Summary</label>
            <textarea
              v-model="editableContent.summary"
              rows="5"
              class="form-textarea"
              placeholder="Enter your professional summary..."
            />
          </div>

          <!-- Work Experiences -->
          <div class="form-section">
            <label class="section-label">Work Experience</label>
            <div
              v-for="(exp, idx) in editableContent.experiences"
              :key="idx"
              class="experience-item"
            >
              <div class="experience-title-edit">
                <div class="form-group-inline">
                  <label class="inline-label">Job Title</label>
                  <input
                    v-model="exp.jobTitle"
                    type="text"
                    class="form-input"
                    placeholder="e.g., Senior Software Engineer"
                  />
                </div>
                <div class="form-group-inline">
                  <label class="inline-label">Company</label>
                  <input
                    v-model="exp.companyName"
                    type="text"
                    class="form-input"
                    placeholder="e.g., Google"
                  />
                </div>
              </div>
              <div class="bullet-points">
                <label class="subsection-label">Bullet Points</label>
                <div
                  v-for="(bullet, bidx) in exp.tailored_bullets"
                  :key="bidx"
                  class="bullet-item"
                >
                  <span class="bullet-label">{{ bidx + 1 }}.</span>
                  <textarea
                    v-model="exp.tailored_bullets[bidx]"
                    rows="2"
                    class="form-textarea"
                    placeholder="Enter bullet point..."
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel: PDF Preview -->
      <div class="preview-panel">
        <div class="panel-header">
          <h4 class="panel-title">Live Preview</h4>
        </div>

        <div class="preview-container">
          <div v-if="loadingPdf" class="pdf-loading">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinner">
              <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/>
            </svg>
            <p>Loading preview...</p>
          </div>
          <div v-else-if="pdfError" class="pdf-error">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <p>{{ pdfError }}</p>
            <Button @click="loadPdfPreview" variant="outline" size="sm">Retry</Button>
          </div>
          <iframe
            v-else-if="pdfUrl"
            :src="pdfUrl + '#view=FitH&toolbar=0'"
            class="pdf-viewer"
            title="Resume PDF Preview"
          ></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuth } from '@clerk/vue'
import { Button } from '@/components/ui/button'

const props = defineProps({
  jobApplicationId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['regenerated', 'cancel'])

const auth = useAuth()
const editableContent = ref(null)
const isLoading = ref(true)
const isRegenerating = ref(false)
const error = ref('')
const loadingPdf = ref(false)
const pdfError = ref('')
const pdfUrl = ref('')

onMounted(async () => {
  await fetchEditableContent()
  await loadPdfPreview()
})

onUnmounted(() => {
  if (pdfUrl.value) {
    URL.revokeObjectURL(pdfUrl.value)
  }
})

async function fetchEditableContent() {
  isLoading.value = true
  error.value = ''

  try {
    const token = await auth.getToken.value()
    if (!token) {
      throw new Error('No authentication token')
    }

    const API_URL = import.meta.env.VITE_API_URL || 'https://resume-vault.fly.dev'
    const response = await fetch(`${API_URL}/resumes/${props.jobApplicationId}/extract`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch content')
    }

    const data = await response.json()
    editableContent.value = data
  } catch (err) {
    console.error('Failed to fetch editable content:', err)
    error.value = err.message || 'Failed to load content'
  } finally {
    isLoading.value = false
  }
}

async function handleRegenerate() {
  isRegenerating.value = true

  try {
    const token = await auth.getToken.value()
    if (!token) {
      throw new Error('No authentication token')
    }

    const API_URL = import.meta.env.VITE_API_URL || 'https://resume-vault.fly.dev'
    const response = await fetch(`${API_URL}/resumes/${props.jobApplicationId}/regenerate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        edited_content: editableContent.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Failed to regenerate resume')
    }

    const data = await response.json()
    // Emit with latex_content instead of html_content
    emit('regenerated', {
      latex_content: data.latex_content,
      cover_letter_content: data.cover_letter_content,
      version_number: data.version_number,
      job_application_id: data.job_application_id
    })
  } catch (err) {
    console.error('Failed to regenerate resume:', err)
    alert(err.message || 'Failed to regenerate resume. Please try again.')
  } finally {
    isRegenerating.value = false
  }
}

function handleCancel() {
  emit('cancel')
}

async function loadPdfPreview() {
  loadingPdf.value = true
  pdfError.value = ''

  try {
    const token = await auth.getToken.value()
    if (!token) {
      throw new Error('No authentication token')
    }

    const API_URL = import.meta.env.VITE_API_URL || 'https://resume-vault.fly.dev'
    const response = await fetch(`${API_URL}/resumes/${props.jobApplicationId}/pdf`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error('Failed to load PDF preview')
    }

    const blob = await response.blob()

    // Clean up old URL if exists
    if (pdfUrl.value) {
      URL.revokeObjectURL(pdfUrl.value)
    }

    // Create blob URL for preview
    pdfUrl.value = URL.createObjectURL(blob)
  } catch (error) {
    console.error('Failed to load PDF preview:', error)
    pdfError.value = error.message || 'Failed to load PDF preview. Please try again.'
  } finally {
    loadingPdf.value = false
  }
}

async function handleCompile() {
  isRegenerating.value = true

  try {
    const token = await auth.getToken.value()
    if (!token) {
      throw new Error('No authentication token')
    }

    const API_URL = import.meta.env.VITE_API_URL || 'https://resume-vault.fly.dev'
    const response = await fetch(`${API_URL}/resumes/${props.jobApplicationId}/regenerate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        edited_content: editableContent.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Failed to compile resume')
    }

    const data = await response.json()

    // Reload PDF preview with new version
    await loadPdfPreview()
  } catch (err) {
    console.error('Failed to compile resume:', err)
    alert(err.message || 'Failed to compile resume. Please try again.')
  } finally {
    isRegenerating.value = false
  }
}
</script>

<style scoped>
.edit-form-container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0;
}

.edit-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}

.edit-panel {
  display: flex;
  flex-direction: column;
  max-height: 1180px;
  overflow: hidden;
}

.preview-panel {
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 1rem;
  align-self: start;
  max-height: 1180px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
}

.panel-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.panel-actions {
  display: flex;
  gap: 0.75rem;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 3rem 0;
  color: #6b7280;
}

.error-state p {
  color: #dc2626;
  margin-bottom: 1rem;
}

.edit-form {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  flex: 1;
  padding-right: 0.5rem;
}

.edit-form::-webkit-scrollbar {
  width: 8px;
}

.edit-form::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.edit-form::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.edit-form::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.preview-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.pdf-viewer {
  width: 100%;
  height: 1100px;
  border: none;
  background: #f5f5f5;
  display: block;
}

.pdf-loading,
.pdf-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  gap: 1rem;
  color: #4a4a4a;
  min-height: 400px;
}

.pdf-loading svg,
.pdf-error svg {
  color: #3b82f6;
}

.pdf-error svg {
  color: #dc2626;
}

.pdf-loading p,
.pdf-error p {
  margin: 0;
  font-size: 1rem;
  color: #4a4a4a;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.form-section {
  margin-bottom: 2rem;
}

.section-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 0.75rem;
}

.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.2s;
}

.form-textarea:focus {
  outline: none;
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

.experience-item {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.experience-title-edit {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group-inline {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.inline-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
}

.form-input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #2c5aa0;
  box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
}

.subsection-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #4b5563;
  margin-bottom: 0.75rem;
}

.bullet-points {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bullet-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: start;
}

.bullet-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6b7280;
  padding-top: 0.75rem;
}


/* Responsive */
@media (max-width: 1200px) {
  .edit-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .edit-panel {
    max-height: 980px;
  }

  .preview-panel {
    position: static;
    max-height: 980px;
  }

  .pdf-viewer {
    height: 900px;
  }
}

@media (max-width: 768px) {
  .experience-title-edit {
    grid-template-columns: 1fr;
  }

  .panel-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .panel-actions {
    width: 100%;
    flex-direction: column;
  }

  .panel-actions button {
    width: 100%;
  }

  .edit-panel {
    max-height: 780px;
  }

  .preview-panel {
    max-height: 780px;
  }

  .pdf-viewer {
    height: 700px;
  }
}
</style>
