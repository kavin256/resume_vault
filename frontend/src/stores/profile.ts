import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserProfile } from '../types'
import apiClient from '../api/client'

export const useProfileStore = defineStore('profile', () => {
  const profiles = ref<UserProfile[]>([])
  const currentProfile = ref<UserProfile | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchProfiles() {
    loading.value = true
    error.value = null
    try {
      profiles.value = await apiClient.getProfiles()
      // Auto-select first profile if available
      if (profiles.value.length > 0 && !currentProfile.value) {
        currentProfile.value = profiles.value[0]
      }
    } catch (err) {
      error.value = 'Failed to fetch profiles'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function createProfile(profile: UserProfile) {
    loading.value = true
    error.value = null
    try {
      const newProfile = await apiClient.createProfile(profile)
      profiles.value.push(newProfile)
      currentProfile.value = newProfile
      return newProfile
    } catch (err) {
      error.value = 'Failed to create profile'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(id: number, profile: Partial<UserProfile>) {
    loading.value = true
    error.value = null
    try {
      const updated = await apiClient.updateProfile(id, profile)
      const index = profiles.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        profiles.value[index] = updated
      }
      if (currentProfile.value?.id === id) {
        currentProfile.value = updated
      }
      return updated
    } catch (err) {
      error.value = 'Failed to update profile'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteProfile(id: number) {
    loading.value = true
    error.value = null
    try {
      await apiClient.deleteProfile(id)
      profiles.value = profiles.value.filter((p) => p.id !== id)
      if (currentProfile.value?.id === id) {
        currentProfile.value = profiles.value[0] || null
      }
    } catch (err) {
      error.value = 'Failed to delete profile'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    profiles,
    currentProfile,
    loading,
    error,
    fetchProfiles,
    createProfile,
    updateProfile,
    deleteProfile,
  }
})
