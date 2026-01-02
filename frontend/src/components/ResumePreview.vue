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
      <p class="preview-description">Review your tailored resume below. You can edit the content or download it as PDF.</p>
      <div class="ats-scores-mini">
        <span class="score-badge" :class="getScoreClass(atsScore)">
          ATS Score: {{ atsScore }}%
        </span>
      </div>
    </div>

    <!-- HTML Preview in iframe -->
    <div class="preview-frame-container">
      <iframe
        ref="previewIframe"
        :srcdoc="htmlContent"
        sandbox="allow-same-origin allow-scripts"
        class="preview-iframe"
        title="Resume Preview"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@clerk/vue'
import { Button } from '@/components/ui/button'

const props = defineProps({
  htmlContent: {
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
const previewIframe = ref(null)
const isDownloading = ref(false)

function handleEdit() {
  emit('edit')
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
}

.preview-iframe {
  width: 100%;
  height: 1100px;
  border: none;
  display: block;
  background: white;
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

  .preview-iframe {
    height: 800px;
  }
}
</style>
