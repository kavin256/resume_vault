import axios from 'axios'
import type { AxiosInstance } from 'axios'
import type { UserProfile, Company, Resume, TailorRequest } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  // Profile API
  async getProfiles(): Promise<UserProfile[]> {
    const response = await this.client.get('/api/profiles')
    return response.data
  }

  async getProfile(id: number): Promise<UserProfile> {
    const response = await this.client.get(`/api/profiles/${id}`)
    return response.data
  }

  async createProfile(profile: UserProfile): Promise<UserProfile> {
    const response = await this.client.post('/api/profiles/', profile)
    return response.data
  }

  async updateProfile(id: number, profile: Partial<UserProfile>): Promise<UserProfile> {
    const response = await this.client.put(`/api/profiles/${id}`, profile)
    return response.data
  }

  async deleteProfile(id: number): Promise<void> {
    await this.client.delete(`/api/profiles/${id}`)
  }

  // Company API
  async getCompanies(): Promise<Company[]> {
    const response = await this.client.get('/api/companies')
    return response.data
  }

  async getCompany(id: number): Promise<Company> {
    const response = await this.client.get(`/api/companies/${id}`)
    return response.data
  }

  async createCompany(company: Company): Promise<Company> {
    const response = await this.client.post('/api/companies/', company)
    return response.data
  }

  async updateCompany(id: number, company: Partial<Company>): Promise<Company> {
    const response = await this.client.put(`/api/companies/${id}`, company)
    return response.data
  }

  async deleteCompany(id: number): Promise<void> {
    await this.client.delete(`/api/companies/${id}`)
  }

  // Resume API
  async getResumes(): Promise<Resume[]> {
    const response = await this.client.get('/api/resumes')
    return response.data
  }

  async getResume(id: number): Promise<Resume> {
    const response = await this.client.get(`/api/resumes/${id}`)
    return response.data
  }

  async getResumesByCompany(companyId: number): Promise<Resume[]> {
    const response = await this.client.get(`/api/resumes/company/${companyId}`)
    return response.data
  }

  async tailorResume(request: TailorRequest): Promise<Resume> {
    const response = await this.client.post('/api/resumes/tailor', request)
    return response.data
  }

  async deleteResume(id: number): Promise<void> {
    await this.client.delete(`/api/resumes/${id}`)
  }

  // Utility
  async healthCheck(): Promise<{ status: string; database: string; environment: string }> {
    const response = await this.client.get('/health')
    return response.data
  }
}

export const apiClient = new ApiClient()
export default apiClient
