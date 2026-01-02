<template>
  <div class="pdf-preview-container">
    <div class="preview-header">
      <h3 class="preview-title">Resume Preview (PDF)</h3>
      <div class="preview-actions">
        <Button @click="handleDownloadPDF" variant="default" size="default" :disabled="isDownloading">
          <svg v-if="!isDownloading" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"></path>
          </svg>
          {{ isDownloading ? 'Downloading...' : 'Download PDF' }}
        </Button>
      </div>
    </div>

    <div class="preview-info">
      <p class="preview-description">Your tailored resume is ready. Preview below or download.</p>
      <div class="ats-scores-mini">
        <span class="score-badge" :class="getScoreClass(atsScore)">
          ATS Score: {{ atsScore }}%
        </span>
      </div>
    </div>

    <!-- PDF Preview -->
    <div v-if="pdfUrl" class="pdf-wrapper">
      <embed
        :src="pdfUrl"
        type="application/pdf"
        class="pdf-embed"
        title="Resume PDF Preview"
      />
    </div>

    <!-- Loading State -->
    <div v-else class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading PDF preview...</p>
    </div>

    <!-- Fallback download link for browsers that don't support embed -->
    <div v-if="pdfUrl" class="pdf-fallback">
      <p class="fallback-text">Can't see the PDF preview above?</p>
      <Button @click="handleDownloadPDF" variant="outline" size="sm">
        Download PDF to View
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Button } from '@/components/ui/button'

const props = defineProps({
  pdfBase64: {
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
  },
  companyName: {
    type: String,
    default: 'Company'
  }
})

const emit = defineEmits(['downloaded'])

const isDownloading = ref(false)

// Create PDF URL from base64
const pdfUrl = computed(() => {
  if (!props.pdfBase64) return null
  try {
    const binaryString = atob(props.pdfBase64)
    const len = binaryString.length
    const bytes = new Uint8Array(len)
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i)
    }
    const blob = new Blob([bytes], { type: 'application/pdf' })
    return URL.createObjectURL(blob)
  } catch (error) {
    console.error('Failed to create PDF URL:', error)
    return null
  }
})

// Clean up URL when component unmounts or PDF changes
watch(pdfUrl, (newUrl, oldUrl) => {
  if (oldUrl && oldUrl.startsWith('blob:')) {
    URL.revokeObjectURL(oldUrl)
  }
})

onMounted(() => {
  // Cleanup on unmount
  return () => {
    if (pdfUrl.value && pdfUrl.value.startsWith('blob:')) {
      URL.revokeObjectURL(pdfUrl.value)
    }
  }
})

function handleDownloadPDF() {
  if (!pdfUrl.value) return

  isDownloading.value = true

  // Create download link
  const a = document.createElement('a')
  a.href = pdfUrl.value
  a.download = `resume_${props.companyName.replace(/\s+/g, '_')}.pdf`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)

  emit('downloaded')

  // Reset downloading state after a short delay
  setTimeout(() => {
    isDownloading.value = false
  }, 500)
}

function getScoreClass(score) {
  if (score >= 85) return 'score-excellent'
  if (score >= 75) return 'score-good'
  if (score >= 65) return 'score-fair'
  return 'score-poor'
}
</script>

<style scoped>
.pdf-preview-container {
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

.pdf-wrapper {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: #525659;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.pdf-embed {
  width: 100%;
  height: 1100px;
  border: none;
  display: block;
}

.loading-state {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 80px 40px;
  text-align: center;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 20px;
  border: 4px solid #e0e0e0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

.pdf-fallback {
  margin-top: 1.5rem;
  text-align: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px dashed #cbd5e1;
}

.fallback-text {
  margin: 0 0 1rem 0;
  color: #64748b;
  font-size: 0.95rem;
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

  .preview-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .pdf-embed {
    height: 600px;
  }
}
</style>

