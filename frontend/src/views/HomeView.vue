<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useProfileStore } from '../stores/profile'
import { useCompanyStore } from '../stores/company'
import { useResumeStore } from '../stores/resume'

const profileStore = useProfileStore()
const companyStore = useCompanyStore()
const resumeStore = useResumeStore()

const profileCount = ref(0)
const companyCount = ref(0)
const resumeCount = ref(0)

onMounted(async () => {
  try {
    await Promise.all([
      profileStore.fetchProfiles(),
      companyStore.fetchCompanies(),
      resumeStore.fetchResumes(),
    ])

    profileCount.value = profileStore.profiles.length
    companyCount.value = companyStore.companies.length
    resumeCount.value = resumeStore.resumes.length
  } catch (error) {
    console.error('Error loading stats:', error)
  }
})
</script>

<template>
  <div class="page-header">
    <h1>Welcome to Resume Vault</h1>
    <p>Your 3-step career command center for tailored resumes</p>
  </div>

  <div class="grid grid-2">
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Master Profile</h2>
      </div>
      <p>
        Manage your complete career history, skills, and experience. This is the "No Lies" source
        of truth for all your resume versions.
      </p>
      <div style="margin-top: 1rem">
        <router-link to="/profile" class="btn btn-primary">Manage Profile</router-link>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Company Vault</h2>
      </div>
      <p>
        Track companies you're interested in, save job descriptions, and generate tailored resumes
        for each position.
      </p>
      <div style="margin-top: 1rem">
        <router-link to="/companies" class="btn btn-primary">View Companies</router-link>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-header">
      <h2 class="card-title">Quick Stats</h2>
    </div>
    <div style="display: flex; gap: 2rem; flex-wrap: wrap">
      <div style="flex: 1; min-width: 200px">
        <div style="font-size: 2rem; font-weight: bold; color: var(--primary-color)">
          {{ profileCount }}
        </div>
        <div style="color: var(--text-secondary)">Master Profiles</div>
      </div>
      <div style="flex: 1; min-width: 200px">
        <div style="font-size: 2rem; font-weight: bold; color: var(--secondary-color)">
          {{ companyCount }}
        </div>
        <div style="color: var(--text-secondary)">Companies Tracked</div>
      </div>
      <div style="flex: 1; min-width: 200px">
        <div style="font-size: 2rem; font-weight: bold; color: var(--warning-color)">
          {{ resumeCount }}
        </div>
        <div style="color: var(--text-secondary)">Tailored Resumes</div>
      </div>
    </div>
  </div>
</template>
