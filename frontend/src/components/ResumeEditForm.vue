<template>
  <div class="edit-form-container">
    <div class="edit-header">
      <h3 class="edit-title">Edit Resume Content</h3>
      <p class="edit-description">Make changes to your resume content. The styling will be preserved when regenerated.</p>
    </div>

    <div v-if="isLoading" class="loading-state">
      <p>Loading content...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <Button @click="handleCancel" variant="outline">Go Back</Button>
    </div>

    <div v-else-if="editableContent" class="edit-form">
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
          <h4 class="experience-header">
            {{ exp.jobTitle }} at {{ exp.company }}
          </h4>
          <div class="bullet-points">
            <div
              v-for="(bullet, bidx) in exp.bullets"
              :key="bidx"
              class="bullet-item"
            >
              <span class="bullet-label">Bullet {{ bidx + 1 }}:</span>
              <textarea
                v-model="exp.bullets[bidx]"
                rows="2"
                class="form-textarea"
                placeholder="Enter bullet point..."
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Skills -->
      <div class="form-section">
        <label class="section-label">Skills</label>
        <textarea
          v-model="editableContent.skills"
          rows="3"
          class="form-textarea"
          placeholder="Enter skills (comma-separated)..."
        />
      </div>

      <!-- Education -->
      <div class="form-section">
        <label class="section-label">Education</label>
        <textarea
          v-model="editableContent.education"
          rows="3"
          class="form-textarea"
          placeholder="Enter education details..."
        />
      </div>

      <!-- Action Buttons -->
      <div class="form-actions">
        <Button @click="handleCancel" variant="outline" :disabled="isRegenerating">
          Cancel
        </Button>
        <Button @click="handleRegenerate" variant="default" :disabled="isRegenerating">
          {{ isRegenerating ? 'Regenerating...' : 'Regenerate Resume' }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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

onMounted(async () => {
  await fetchEditableContent()
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
    emit('regenerated', data)
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
</script>

<style scoped>
.edit-form-container {
  margin-top: 2rem;
}

.edit-header {
  margin-bottom: 2rem;
}

.edit-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 0.5rem 0;
}

.edit-description {
  color: #6b7280;
  margin: 0;
  font-size: 0.95rem;
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
  max-width: 900px;
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

.experience-header {
  font-size: 1rem;
  font-weight: 600;
  color: #2c5aa0;
  margin: 0 0 1rem 0;
}

.bullet-points {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bullet-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bullet-label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #6b7280;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.form-actions button {
  min-width: 140px;
}

/* Responsive */
@media (max-width: 768px) {
  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions button {
    width: 100%;
  }
}
</style>
