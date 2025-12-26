import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Company } from '../types'
import apiClient from '../api/client'

export const useCompanyStore = defineStore('company', () => {
  const companies = ref<Company[]>([])
  const currentCompany = ref<Company | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchCompanies() {
    loading.value = true
    error.value = null
    try {
      companies.value = await apiClient.getCompanies()
    } catch (err) {
      error.value = 'Failed to fetch companies'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  async function fetchCompany(id: number) {
    loading.value = true
    error.value = null
    try {
      currentCompany.value = await apiClient.getCompany(id)
      return currentCompany.value
    } catch (err) {
      error.value = 'Failed to fetch company'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCompany(company: Company) {
    loading.value = true
    error.value = null
    try {
      const newCompany = await apiClient.createCompany(company)
      companies.value.unshift(newCompany)
      return newCompany
    } catch (err) {
      error.value = 'Failed to create company'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCompany(id: number, company: Partial<Company>) {
    loading.value = true
    error.value = null
    try {
      const updated = await apiClient.updateCompany(id, company)
      const index = companies.value.findIndex((c) => c.id === id)
      if (index !== -1) {
        companies.value[index] = updated
      }
      if (currentCompany.value?.id === id) {
        currentCompany.value = updated
      }
      return updated
    } catch (err) {
      error.value = 'Failed to update company'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteCompany(id: number) {
    loading.value = true
    error.value = null
    try {
      await apiClient.deleteCompany(id)
      companies.value = companies.value.filter((c) => c.id !== id)
      if (currentCompany.value?.id === id) {
        currentCompany.value = null
      }
    } catch (err) {
      error.value = 'Failed to delete company'
      console.error(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    companies,
    currentCompany,
    loading,
    error,
    fetchCompanies,
    fetchCompany,
    createCompany,
    updateCompany,
    deleteCompany,
  }
})
