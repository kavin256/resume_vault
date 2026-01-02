<template>
  <div class="resume-preview-container">
    <div class="preview-header">
      <h3 class="preview-title">Resume Preview (LaTeX)</h3>
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
      <p class="preview-description">Review your LaTeX source below. Click "Download PDF" to compile and download the formatted resume.</p>
      <div class="ats-scores-mini">
        <span class="score-badge" :class="getScoreClass(atsScore)">
          ATS Score: {{ atsScore }}%
        </span>
      </div>
    </div>

    <!-- LaTeX Source Code Display -->
    <div class="preview-frame-container">
      <div class="latex-source-container">
        <div class="source-header">
          <span class="source-label">LaTeX Source Code</span>
          <button @click="copyToClipboard" class="copy-button" :class="{ 'copied': isCopied }">
            <svg v-if="!isCopied" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"></path>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            {{ isCopied ? 'Copied!' : 'Copy' }}
          </button>
        </div>
        <pre class="latex-source"><code>{{ latexContent }}</code></pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
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
const isCopied = ref(false)

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

async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(props.latexContent)
    isCopied.value = true
    setTimeout(() => {
      isCopied.value = false
    }, 2000)
  } catch (error) {
    console.error('Failed to copy:', error)
  }
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

.latex-source-container {
  background: #1e1e1e;
  color: #d4d4d4;
  border-radius: 8px;
  overflow: hidden;
}

.source-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #2d2d2d;
  border-bottom: 1px solid #3e3e3e;
}

.source-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #9cdcfe;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.copy-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #3e3e3e;
  border: 1px solid #4e4e4e;
  border-radius: 4px;
  color: #d4d4d4;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-button:hover {
  background: #4e4e4e;
  border-color: #5e5e5e;
}

.copy-button.copied {
  background: #16a34a;
  border-color: #16a34a;
  color: white;
}

.latex-source {
  margin: 0;
  padding: 20px;
  overflow-x: auto;
  max-height: 800px;
  overflow-y: auto;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  background: #1e1e1e;
  color: #d4d4d4;
}

.latex-source code {
  font-family: inherit;
  color: inherit;
}

/* Scrollbar styling for dark theme */
.latex-source::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

.latex-source::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.latex-source::-webkit-scrollbar-thumb {
  background: #4e4e4e;
  border-radius: 5px;
}

.latex-source::-webkit-scrollbar-thumb:hover {
  background: #5e5e5e;
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

  .latex-source {
    font-size: 11px;
    padding: 12px;
    max-height: 600px;
  }
}
</style>
