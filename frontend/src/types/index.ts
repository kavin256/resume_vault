// TypeScript types for Resume Vault

export interface UserProfile {
  id?: number
  full_name: string
  email: string
  phone?: string
  location?: string
  linkedin_url?: string
  portfolio_url?: string
  github_url?: string
  professional_summary?: string
  work_experience?: string
  education?: string
  technical_skills?: string
  soft_skills?: string
  certifications?: string
  projects?: string
  achievements?: string
  languages?: string
  publications?: string
  volunteer_work?: string
  created_at?: string
  updated_at?: string
}

export interface Company {
  id?: number
  company_name: string
  industry?: string
  company_website?: string
  company_description?: string
  job_title: string
  job_description: string
  job_requirements?: string
  job_url?: string
  application_status?: ApplicationStatus
  application_date?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

export interface Resume {
  id?: number
  company_id: number
  resume_version?: string
  resume_title?: string
  resume_content: string
  resume_format?: string
  ai_model_used?: string
  generation_prompt?: string
  keywords_targeted?: string
  sections_included?: string
  skills_highlighted?: string
  experiences_featured?: string
  is_active?: boolean
  is_sent?: boolean
  sent_at?: string
  file_path?: string
  file_url?: string
  created_at?: string
  updated_at?: string
}

export type ApplicationStatus =
  | 'not_applied'
  | 'applied'
  | 'interviewing'
  | 'offer'
  | 'rejected'

export interface TailorRequest {
  company_id: number
  profile_id?: number
}

export interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
}
