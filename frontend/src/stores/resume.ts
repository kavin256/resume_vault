import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Resume, TailorRequest } from '../types'
import apiClient from '../api/client'

export const useResumeStore = defineStore('resume', () => {
  const resumes = ref<Resume[]>([])
  const currentResume = ref<Resume | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchResumes() {
    loading.value = true
    error.value = null
    try {
      resumes.value = await apiClient.getResumes()
    } catch (err) {
      error.value = 'Failed to fetch resumes'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function fetchResume(id: number) {
    loading.value = true
    error.value = null
    try {
      currentResume.value = await apiClient.getResume(id)
      return currentResume.value
    } catch (err) {
      error.value = 'Failed to fetch resume'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchResumesByCompany(companyId: number) {
    loading.value = true
    error.value = null
    try {
      const companyResumes = await apiClient.getResumesByCompany(companyId)
      return companyResumes
    } catch (err) {
      error.value = 'Failed to fetch company resumes'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function tailorResume(request: TailorRequest) {
    loading.value = true
    error.value = null
    try {
      const newResume = await apiClient.tailorResume(request)
      resumes.value.unshift(newResume)
      currentResume.value = newResume
      return newResume
    } catch (err) {
      error.value = 'Failed to tailor resume. Make sure you have created a Master Profile first.'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteResume(id: number) {
    loading.value = true
    error.value = null
    try {
      await apiClient.deleteResume(id)
      resumes.value = resumes.value.filter((r) => r.id !== id)
      if (currentResume.value?.id === id) {
        currentResume.value = null
      }
    } catch (err) {
      error.value = 'Failed to delete resume'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    resumes,
    currentResume,
    loading,
    error,
    fetchResumes,
    fetchResume,
    fetchResumesByCompany,
    tailorResume,
    deleteResume,
  }
})
