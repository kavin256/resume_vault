<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useProfileStore } from '../stores/profile'
import type { UserProfile } from '../types'

const profileStore = useProfileStore()
const showAlert = ref(false)
const alertMessage = ref('')
const alertType = ref<'success' | 'error'>('success')

const formData = ref<UserProfile>({
  full_name: '',
  email: '',
  phone: '',
  location: '',
  linkedin_url: '',
  portfolio_url: '',
  github_url: '',
  professional_summary: '',
  work_experience: '',
  education: '',
  technical_skills: '',
  soft_skills: '',
  certifications: '',
  projects: '',
  achievements: '',
  languages: '',
  publications: '',
  volunteer_work: '',
})

const isEditing = computed(() => !!profileStore.currentProfile?.id)

onMounted(async () => {
  await profileStore.fetchProfiles()
  if (profileStore.currentProfile) {
    formData.value = { ...profileStore.currentProfile }
  }
})

async function saveProfile() {
  try {
    if (isEditing.value && profileStore.currentProfile?.id) {
      await profileStore.updateProfile(profileStore.currentProfile.id, formData.value)
      displayAlert('Profile updated successfully!', 'success')
    } else {
      await profileStore.createProfile(formData.value)
      displayAlert('Profile created successfully!', 'success')
    }
  } catch (error) {
    displayAlert('Failed to save profile. Please try again.', 'error')
  }
}

function loadProfile() {
  if (profileStore.currentProfile) {
    formData.value = { ...profileStore.currentProfile }
    displayAlert('Profile reloaded', 'success')
  }
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
  <div class="page-header">
    <h1>Master Profile</h1>
    <p>Your complete, truthful career history - the source of truth for all resume versions</p>
  </div>

  <div v-if="showAlert" :class="`alert alert-${alertType}`">
    {{ alertMessage }}
  </div>

  <div class="card">
    <form @submit.prevent="saveProfile">
      <h3>Personal Information</h3>
      <div class="grid grid-2">
        <div class="form-group">
          <label for="full_name">Full Name *</label>
          <input type="text" id="full_name" v-model="formData.full_name" required />
        </div>
        <div class="form-group">
          <label for="email">Email *</label>
          <input type="email" id="email" v-model="formData.email" required />
        </div>
      </div>

      <div class="grid grid-2">
        <div class="form-group">
          <label for="phone">Phone</label>
          <input type="tel" id="phone" v-model="formData.phone" />
        </div>
        <div class="form-group">
          <label for="location">Location</label>
          <input type="text" id="location" v-model="formData.location" placeholder="City, State/Country" />
        </div>
      </div>

      <h3 style="margin-top: 2rem">Online Presence</h3>
      <div class="grid grid-2">
        <div class="form-group">
          <label for="linkedin_url">LinkedIn URL</label>
          <input type="url" id="linkedin_url" v-model="formData.linkedin_url" placeholder="https://linkedin.com/in/..." />
        </div>
        <div class="form-group">
          <label for="portfolio_url">Portfolio URL</label>
          <input type="url" id="portfolio_url" v-model="formData.portfolio_url" />
        </div>
      </div>

      <div class="form-group">
        <label for="github_url">GitHub URL</label>
        <input type="url" id="github_url" v-model="formData.github_url" placeholder="https://github.com/..." />
      </div>

      <h3 style="margin-top: 2rem">Professional Summary</h3>
      <div class="form-group">
        <label for="professional_summary">Professional Summary</label>
        <textarea id="professional_summary" v-model="formData.professional_summary" placeholder="A brief overview of your career, key achievements, and what you're looking for..."></textarea>
      </div>

      <h3 style="margin-top: 2rem">Work Experience</h3>
      <div class="form-group">
        <label for="work_experience">Work Experience</label>
        <textarea id="work_experience" v-model="formData.work_experience" style="min-height: 200px" placeholder="List your work experience with company names, positions, dates, and responsibilities...

Example:
Software Engineer | TechCorp Inc. | Jan 2020 - Present
- Developed scalable web applications using React and Node.js
- Led a team of 3 engineers..."></textarea>
      </div>

      <h3 style="margin-top: 2rem">Education</h3>
      <div class="form-group">
        <label for="education">Education</label>
        <textarea id="education" v-model="formData.education" placeholder="List your educational background...

Example:
Bachelor of Science in Computer Science | University Name | 2016-2020
- GPA: 3.8/4.0
- Relevant coursework: Data Structures, Algorithms, Machine Learning"></textarea>
      </div>

      <h3 style="margin-top: 2rem">Skills</h3>
      <div class="grid grid-2">
        <div class="form-group">
          <label for="technical_skills">Technical Skills</label>
          <textarea id="technical_skills" v-model="formData.technical_skills" placeholder="Python, JavaScript, React, Node.js, PostgreSQL, AWS, Docker, Git..."></textarea>
        </div>
        <div class="form-group">
          <label for="soft_skills">Soft Skills</label>
          <textarea id="soft_skills" v-model="formData.soft_skills" placeholder="Leadership, Communication, Problem-solving, Team collaboration..."></textarea>
        </div>
      </div>

      <h3 style="margin-top: 2rem">Additional Information</h3>
      <div class="form-group">
        <label for="certifications">Certifications</label>
        <textarea id="certifications" v-model="formData.certifications" placeholder="List relevant certifications..."></textarea>
      </div>

      <div class="form-group">
        <label for="projects">Projects</label>
        <textarea id="projects" v-model="formData.projects" style="min-height: 150px" placeholder="Describe key projects you've worked on..."></textarea>
      </div>

      <div class="form-group">
        <label for="achievements">Achievements</label>
        <textarea id="achievements" v-model="formData.achievements" placeholder="Awards, recognitions, significant accomplishments..."></textarea>
      </div>

      <div class="form-group">
        <label for="languages">Languages</label>
        <textarea id="languages" v-model="formData.languages" placeholder="Programming languages: Python, JavaScript...
Spoken languages: English (native), Spanish (fluent)..."></textarea>
      </div>

      <div class="form-group">
        <label for="publications">Publications</label>
        <textarea id="publications" v-model="formData.publications" placeholder="Research papers, blog posts, articles..."></textarea>
      </div>

      <div class="form-group">
        <label for="volunteer_work">Volunteer Work</label>
        <textarea id="volunteer_work" v-model="formData.volunteer_work" placeholder="Community involvement, volunteer positions..."></textarea>
      </div>

      <div style="display: flex; gap: 1rem; margin-top: 2rem">
        <button type="submit" class="btn btn-primary" :disabled="profileStore.loading">
          {{ isEditing ? 'Update Profile' : 'Save Profile' }}
        </button>
        <button type="button" class="btn btn-outline" @click="loadProfile" :disabled="!isEditing">
          Reload
        </button>
      </div>
    </form>
  </div>
</template>
