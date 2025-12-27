<template>
  <div class="download-links">
    <h2>Downloads Ready</h2>
    <div class="buttons">
      <button @click="downloadResume" class="download-btn">
        Download Resume (PDF)
      </button>
      <button @click="downloadCoverLetter" class="download-btn">
        Download Cover Letter (PDF)
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  resumeBase64: {
    type: String,
    required: true
  },
  coverLetterBase64: {
    type: String,
    required: true
  }
})

function downloadResume() {
  downloadFile(props.resumeBase64, 'resume.pdf', 'application/pdf')
}

function downloadCoverLetter() {
  downloadFile(props.coverLetterBase64, 'cover_letter.pdf', 'application/pdf')
}

function downloadFile(base64Data, filename, mimeType) {
  // Decode base64 to binary
  const binaryString = atob(base64Data)
  const bytes = new Uint8Array(binaryString.length)
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i)
  }

  // Create blob and download
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
.download-links {
  border: 1px solid #4caf50;
  padding: 20px;
  border-radius: 8px;
  background: #e8f5e9;
  margin-top: 20px;
}

.buttons {
  display: flex;
  gap: 15px;
}

.download-btn {
  padding: 12px 24px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.download-btn:hover {
  background: #45a049;
}
</style>
