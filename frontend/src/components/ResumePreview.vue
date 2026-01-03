<template>
  <div class="resume-preview-container">
    <div class="preview-header">
      <h3 class="preview-title">Resume Preview</h3>
      <div class="preview-actions">
        <Button @click="handleEdit" variant="outline" size="default">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
          Edit Content
        </Button>
        <Button @click="handleDownloadPDF" variant="default" size="default" :disabled="isDownloading">
          <svg v-if="!isDownloading" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"></path>
          </svg>
          {{ isDownloading ? 'Downloading...' : 'Download PDF' }}
        </Button>
      </div>
    </div>

    <div class="preview-info">
      <p class="preview-description">Review your resume PDF below. Click "Edit Content" to modify or "Download PDF" to save.</p>
      <div class="ats-scores-mini">
        <span class="score-badge" :class="getScoreClass(atsScore)">
          ATS Score: {{ atsScore }}%
        </span>
      </div>
    </div>

    <!-- PDF Preview -->
    <div class="preview-frame-container">
      <div v-if="loadingPdf" class="pdf-loading">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinner">
          <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/>
        </svg>
        <p>Loading PDF preview...</p>
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
        :src="pdfUrl"
        class="pdf-viewer"
        title="Resume PDF Preview"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useAuth } from '@clerk/vue'
import { Button } from '@/components/ui/button'

const props = defineProps({
  latexContent: {
    type: String,
    required: true
  },
  jobApplicationId: {
    type: String,
    required: true
  },
  atsScore: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['edit', 'downloaded'])

const auth = useAuth()
const isDownloading = ref(false)
const loadingPdf = ref(false)
const pdfError = ref('')
const pdfUrl = ref('')

function handleEdit() {
  emit('edit')
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

async function handleDownloadPDF() {
  isDownloading.value = true

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
      throw new Error('Failed to download PDF')
    }

    const blob = await response.blob()

    // Trigger browser download
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'resume.pdf'
    a.click()
    URL.revokeObjectURL(url)

    emit('downloaded')
  } catch (error) {
    console.error('Failed to download PDF:', error)
    alert('Failed to download PDF. Please try again.')
  } finally {
    isDownloading.value = false
  }
}

function getScoreClass(score) {
  if (score >= 85) return 'score-excellent'
  if (score >= 75) return 'score-good'
  if (score >= 65) return 'score-fair'
  return 'score-poor'
}

// Load PDF preview when component mounts
onMounted(() => {
  loadPdfPreview()
})

// Watch for jobApplicationId changes and reload preview
watch(() => props.jobApplicationId, () => {
  loadPdfPreview()
})

// Clean up blob URL when component unmounts
onUnmounted(() => {
  if (pdfUrl.value) {
    URL.revokeObjectURL(pdfUrl.value)
  }
})
</script>

<style scoped>
.resume-preview-container {
  margin-top: 2rem;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.preview-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.preview-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.preview-actions button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.preview-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  flex-wrap: wrap;
  gap: 1rem;
}

.preview-description {
  margin: 0;
  color: #4a4a4a;
  font-size: 0.95rem;
}

.ats-scores-mini {
  display: flex;
  gap: 0.5rem;
}

.score-badge {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
}

.score-excellent {
  background: #d4edda;
  color: #155724;
}

.score-good {
  background: #d1ecf1;
  color: #0c5460;
}

.score-fair {
  background: #fff3cd;
  color: #856404;
}

.score-poor {
  background: #f8d7da;
  color: #721c24;
}

.preview-frame-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  max-width: 900px;
  margin: 0 auto;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pdf-viewer {
  width: 100%;
  height: 800px;
  border: none;
  background: #f5f5f5;
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

/* Responsive */
@media (max-width: 768px) {
  .preview-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .preview-actions {
    width: 100%;
  }

  .preview-actions button {
    flex: 1;
  }

  .pdf-viewer {
    height: 600px;
  }

  .preview-frame-container {
    min-height: 400px;
  }
}
</style>
