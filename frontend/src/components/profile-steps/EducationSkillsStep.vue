<template>
  <div class="step-content">
    <div class="step-header-actions">
      <div>
        <h2 class="step-title">Education & Skills</h2>
        <p class="step-description">
          Add your educational background, skills, certifications, and
          publications
        </p>
      </div>
      <Button @click="fillDummyData" variant="outline" class="dummy-data-btn">
        <span class="icon">✨</span>
        Fill with Test Data
      </Button>
    </div>

    <!-- Education -->
    <Card class="form-card section-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <div class="section-title-with-icon">
            <svg
              class="section-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
              <path d="M6 12v5c3 3 9 3 12 0v-5" />
            </svg>
            <h3 class="form-section-title">Education</h3>
          </div>
          <Dialog
            :open="educationDialogOpen"
            @update:open="onEducationDialogChange"
          >
            <DialogTrigger>
              <Button size="sm" variant="outline" class="add-item-btn">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="btn-icon"
                >
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v8" />
                  <path d="M8 12h8" />
                </svg>
                Add Education
              </Button>
            </DialogTrigger>
            <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>{{
                  editingEducationIndex !== null
                    ? "Edit Education"
                    : "Add Education"
                }}</DialogTitle>
                <DialogDescription>
                  {{
                    editingEducationIndex !== null
                      ? "Update your educational background and qualifications."
                      : "Add your educational background and qualifications."
                  }}
                </DialogDescription>
              </DialogHeader>
              <form @submit="onEducationSubmit" class="dialog-form">
                <div class="form-row">
                  <div class="form-group">
                    <label>Institution <span class="required">*</span></label>
                    <input
                      v-model="educationForm.institution"
                      type="text"
                      required
                      placeholder="Stanford University"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>

                  <div class="form-group">
                    <label>Degree <span class="required">*</span></label>
                    <input
                      v-model="educationForm.degree"
                      type="text"
                      required
                      placeholder="Bachelor of Science"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>Field of Study</label>
                    <input
                      v-model="educationForm.fieldOfStudy"
                      type="text"
                      placeholder="Computer Science"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>

                  <div class="form-group">
                    <label>Grade/GPA</label>
                    <input
                      v-model="educationForm.grade"
                      type="text"
                      placeholder="3.8/4.0"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>Start Year</label>
                    <input
                      v-model="educationForm.startYear"
                      type="text"
                      placeholder="2014"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>

                  <div class="form-group">
                    <label>End Year</label>
                    <input
                      v-model="educationForm.endYear"
                      type="text"
                      placeholder="2018"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>
                </div>

                <div class="form-group">
                  <label>Description</label>
                  <textarea
                    v-model="educationForm.description"
                    rows="3"
                    placeholder="Relevant coursework, honors, activities..."
                    class="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  ></textarea>
                </div>

                <DialogFooter>
                  <Button
                    @click="educationDialogOpen = false"
                    variant="outline"
                    type="button"
                  >
                    Cancel
                  </Button>
                  <Button type="submit" :disabled="isSavingEducation">
                    {{
                      isSavingEducation
                        ? "Saving..."
                        : editingEducationIndex !== null
                        ? "Update Education"
                        : "Add Education"
                    }}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <!-- Education List -->
        <div v-if="formData.education.length > 0" class="education-list">
          <div
            v-for="(edu, index) in formData.education"
            :key="index"
            class="education-item"
          >
            <div class="education-header">
              <h3 class="education-title">{{ edu.degree }}</h3>
              <div class="action-buttons">
                <Button
                  @click="editEducation(index)"
                  size="sm"
                  variant="ghost"
                  class="edit-btn"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"
                    />
                    <path d="m15 5 4 4" />
                  </svg>
                </Button>
                <Button
                  @click="removeEducation(index)"
                  size="sm"
                  variant="ghost"
                  class="delete-btn"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M3 6h18" />
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                  </svg>
                </Button>
              </div>
            </div>
            <p class="education-institution">{{ edu.institution }}</p>
            <p class="education-meta">
              {{ edu.fieldOfStudy }}
              <span v-if="edu.grade"> • {{ edu.grade }}</span>
              <span v-if="edu.startYear || edu.endYear">
                • {{ edu.startYear }} - {{ edu.endYear }}
              </span>
            </p>
            <p v-if="edu.description" class="education-description">
              {{ edu.description }}
            </p>
            <hr
              v-if="index < formData.education.length - 1"
              class="education-divider"
            />
          </div>
        </div>

        <div v-else class="empty-state">
          <p>No education added yet. Click "Add Education" to get started.</p>
        </div>
      </CardContent>
    </Card>

    <!-- Skills -->
    <Card class="form-card section-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <div class="section-title-with-icon">
            <svg
              class="section-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"
              />
              <path d="M9 18h6" />
              <path d="M10 22h4" />
            </svg>
            <h3 class="form-section-title">Skills</h3>
          </div>
          <Dialog
            :open="skillDialogOpen"
            @update:open="skillDialogOpen = $event"
          >
            <DialogTrigger>
              <Button size="sm" variant="outline" class="add-item-btn">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="btn-icon"
                >
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v8" />
                  <path d="M8 12h8" />
                </svg>
                Add Skill
              </Button>
            </DialogTrigger>
            <DialogContent class="max-w-md">
              <DialogHeader>
                <DialogTitle>Add Skill</DialogTitle>
                <DialogDescription>
                  Add a skill to your profile.
                </DialogDescription>
              </DialogHeader>
              <form @submit="onSkillSubmit" class="dialog-form">
                <div class="form-group">
                  <label>Skill Name <span class="required">*</span></label>
                  <input
                    v-model="skillForm.name"
                    type="text"
                    required
                    placeholder="JavaScript"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                </div>

                <DialogFooter>
                  <Button
                    @click="skillDialogOpen = false"
                    variant="outline"
                    type="button"
                  >
                    Cancel
                  </Button>
                  <Button type="submit">Add Skill</Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <!-- Skills List -->
        <div v-if="formData.skills.length > 0" class="skills-container">
          <div
            v-for="(skill, index) in formData.skills"
            :key="index"
            class="skill-badge"
          >
            <span>{{ skill.name }}</span>
            <button
              @click="removeSkill(index)"
              type="button"
              class="skill-remove"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M18 6 6 18" />
                <path d="m6 6 12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>No skills added yet. Click "Add Skill" to get started.</p>
        </div>
      </CardContent>
    </Card>

    <!-- Certifications -->
    <Card class="form-card section-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <div class="section-title-with-icon">
            <svg
              class="section-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
              <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
              <path d="M4 22h16" />
              <path
                d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"
              />
              <path
                d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"
              />
              <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z" />
            </svg>
            <h3 class="form-section-title">Certifications</h3>
          </div>
          <Dialog
            :open="certificationDialogOpen"
            @update:open="onCertificationDialogChange"
          >
            <DialogTrigger>
              <Button size="sm" variant="outline" class="add-item-btn">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="btn-icon"
                >
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v8" />
                  <path d="M8 12h8" />
                </svg>
                Add Certification
              </Button>
            </DialogTrigger>
            <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>{{
                  editingCertificationIndex !== null
                    ? "Edit Certification"
                    : "Add Certification"
                }}</DialogTitle>
                <DialogDescription>
                  {{
                    editingCertificationIndex !== null
                      ? "Update your certification details."
                      : "Add your certification details."
                  }}
                </DialogDescription>
              </DialogHeader>
              <form @submit="onCertificationSubmit" class="dialog-form">
                <div class="form-group">
                  <label
                    >Certification Name <span class="required">*</span></label
                  >
                  <input
                    v-model="certificationForm.name"
                    type="text"
                    required
                    placeholder="AWS Certified Solutions Architect"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>Issuing Organization</label>
                    <input
                      v-model="certificationForm.issuingOrganization"
                      type="text"
                      placeholder="Amazon Web Services"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>

                  <div class="form-group">
                    <label>Issue Date</label>
                    <input
                      v-model="certificationForm.issueDate"
                      type="month"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>Expiration Date</label>
                    <input
                      v-model="certificationForm.expirationDate"
                      type="month"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>

                  <div class="form-group">
                    <label>Credential ID</label>
                    <input
                      v-model="certificationForm.credentialId"
                      type="text"
                      placeholder="ABC123XYZ"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>
                </div>

                <div class="form-group">
                  <label>Credential URL</label>
                  <input
                    v-model="certificationForm.credentialUrl"
                    type="url"
                    placeholder="https://..."
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                </div>

                <DialogFooter>
                  <Button
                    @click="certificationDialogOpen = false"
                    variant="outline"
                    type="button"
                  >
                    Cancel
                  </Button>
                  <Button type="submit" :disabled="isSavingCertification">
                    {{
                      isSavingCertification
                        ? "Saving..."
                        : editingCertificationIndex !== null
                        ? "Update Certification"
                        : "Add Certification"
                    }}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <!-- Certifications List -->
        <div
          v-if="formData.certifications.length > 0"
          class="certifications-list"
        >
          <div
            v-for="(cert, index) in formData.certifications"
            :key="index"
            class="certification-item"
          >
            <div class="certification-header">
              <h3 class="certification-title">{{ cert.name }}</h3>
              <div class="action-buttons">
                <Button
                  @click="editCertification(index)"
                  size="sm"
                  variant="ghost"
                  class="edit-btn"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"
                    />
                    <path d="m15 5 4 4" />
                  </svg>
                </Button>
                <Button
                  @click="removeCertification(index)"
                  size="sm"
                  variant="ghost"
                  class="delete-btn"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M3 6h18" />
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                  </svg>
                </Button>
              </div>
            </div>
            <p class="certification-organization">
              {{ cert.issuingOrganization }}
            </p>
            <p class="certification-meta">
              <span v-if="cert.issueDate"
                >Issued: {{ formatMonthYear(cert.issueDate) }}</span
              >
              <span v-if="cert.expirationDate">
                • Expires: {{ formatMonthYear(cert.expirationDate) }}</span
              >
              <span v-if="!cert.expirationDate && cert.issueDate">
                • No Expiration</span
              >
            </p>
            <p v-if="cert.credentialId" class="certification-credential">
              Credential ID: {{ cert.credentialId }}
            </p>
            <p v-if="cert.credentialUrl" class="certification-url">
              <a
                :href="cert.credentialUrl"
                target="_blank"
                rel="noopener noreferrer"
              >
                View Credential
              </a>
            </p>
            <hr
              v-if="index < formData.certifications.length - 1"
              class="certification-divider"
            />
          </div>
        </div>

        <div v-else class="empty-state">
          <p>
            No certifications added yet. Click "Add Certification" to get
            started.
          </p>
        </div>
      </CardContent>
    </Card>

    <!-- Publications -->
    <Card class="form-card section-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <div class="section-title-with-icon">
            <svg
              class="section-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
              />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" x2="8" y1="13" y2="13" />
              <line x1="16" x2="8" y1="17" y2="17" />
              <line x1="10" x2="8" y1="9" y2="9" />
            </svg>
            <h3 class="form-section-title">Publications</h3>
          </div>
          <Dialog
            :open="publicationDialogOpen"
            @update:open="onPublicationDialogChange"
          >
            <DialogTrigger>
              <Button size="sm" variant="outline" class="add-item-btn">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="btn-icon"
                >
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v8" />
                  <path d="M8 12h8" />
                </svg>
                Add Publication
              </Button>
            </DialogTrigger>
            <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>{{
                  editingPublicationIndex !== null
                    ? "Edit Publication"
                    : "Add Publication"
                }}</DialogTitle>
                <DialogDescription>
                  {{
                    editingPublicationIndex !== null
                      ? "Update your publication details."
                      : "Add your publication details."
                  }}
                </DialogDescription>
              </DialogHeader>
              <form @submit="onPublicationSubmit" class="dialog-form">
                <div class="form-group">
                  <label>Title <span class="required">*</span></label>
                  <input
                    v-model="publicationForm.title"
                    type="text"
                    required
                    placeholder="Research Paper Title"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>Publisher</label>
                    <input
                      v-model="publicationForm.publisher"
                      type="text"
                      placeholder="IEEE, ACM, etc."
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>

                  <div class="form-group">
                    <label>Publication Date</label>
                    <input
                      v-model="publicationForm.publicationDate"
                      type="month"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>
                </div>

                <div class="form-group">
                  <label>URL</label>
                  <input
                    v-model="publicationForm.url"
                    type="url"
                    placeholder="https://..."
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                </div>

                <DialogFooter>
                  <Button
                    @click="publicationDialogOpen = false"
                    variant="outline"
                    type="button"
                  >
                    Cancel
                  </Button>
                  <Button type="submit" :disabled="isSavingPublication">
                    {{
                      isSavingPublication
                        ? "Saving..."
                        : editingPublicationIndex !== null
                        ? "Update Publication"
                        : "Add Publication"
                    }}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <!-- Publications List -->
        <div v-if="formData.publications.length > 0" class="publications-list">
          <div
            v-for="(pub, index) in formData.publications"
            :key="index"
            class="publication-item"
          >
            <div class="publication-header">
              <h3 class="publication-title">{{ pub.title }}</h3>
              <div class="action-buttons">
                <Button
                  @click="editPublication(index)"
                  size="sm"
                  variant="ghost"
                  class="edit-btn"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"
                    />
                    <path d="m15 5 4 4" />
                  </svg>
                </Button>
                <Button
                  @click="removePublication(index)"
                  size="sm"
                  variant="ghost"
                  class="delete-btn"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M3 6h18" />
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                  </svg>
                </Button>
              </div>
            </div>
            <p v-if="pub.publisher" class="publication-publisher">
              {{ pub.publisher }}
            </p>
            <p v-if="pub.publicationDate" class="publication-meta">
              Published: {{ formatMonthYear(pub.publicationDate) }}
            </p>
            <p v-if="pub.url" class="publication-url">
              <a :href="pub.url" target="_blank" rel="noopener noreferrer">
                View Publication
              </a>
            </p>
            <hr
              v-if="index < formData.publications.length - 1"
              class="publication-divider"
            />
          </div>
        </div>

        <div v-else class="empty-state">
          <p>
            No publications added yet. Click "Add Publication" to get started.
          </p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from "vue";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue"]);

const formData = props.modelValue;

// Education
const educationDialogOpen = ref(false);
const isSavingEducation = ref(false);
const editingEducationIndex = ref(null);

const educationForm = ref({
  institution: "",
  degree: "",
  fieldOfStudy: "",
  startYear: "",
  endYear: "",
  grade: "",
  description: "",
});

function resetEducationForm() {
  educationForm.value = {
    institution: "",
    degree: "",
    fieldOfStudy: "",
    startYear: "",
    endYear: "",
    grade: "",
    description: "",
  };
  editingEducationIndex.value = null;
}

async function onEducationSubmit(event) {
  event.preventDefault();
  isSavingEducation.value = true;

  try {
    if (editingEducationIndex.value !== null) {
      // Update existing education
      formData.education[editingEducationIndex.value] = {
        ...educationForm.value,
      };
    } else {
      // Add new education
      formData.education.push({ ...educationForm.value });
    }

    // Reset form and close dialog
    resetEducationForm();
    educationDialogOpen.value = false;
  } catch (error) {
    console.error("Error saving education:", error);
    alert("Failed to save education. Please try again.");
  } finally {
    isSavingEducation.value = false;
  }
}

function editEducation(index) {
  const edu = formData.education[index];
  educationForm.value = { ...edu };
  editingEducationIndex.value = index;
  educationDialogOpen.value = true;
}

function onEducationDialogChange(isOpen) {
  educationDialogOpen.value = isOpen;
  // Reset form when opening dialog for adding (not editing)
  if (isOpen && editingEducationIndex.value === null) {
    resetEducationForm();
  }
  // Reset editing state when closing dialog
  if (!isOpen) {
    editingEducationIndex.value = null;
  }
}

function addEducation() {
  formData.education.push({
    institution: "",
    degree: "",
    fieldOfStudy: "",
    startYear: "",
    endYear: "",
    grade: "",
    description: "",
  });
}

function removeEducation(index) {
  formData.education.splice(index, 1);
}

// Skills
const skillDialogOpen = ref(false);
const skillForm = ref({
  name: "",
});

function resetSkillForm() {
  skillForm.value = {
    name: "",
  };
}

async function onSkillSubmit(event) {
  event.preventDefault();

  if (skillForm.value.name.trim()) {
    formData.skills.push({ name: skillForm.value.name.trim() });
    resetSkillForm();
    skillDialogOpen.value = false;
  }
}

function addSkill() {
  formData.skills.push({
    name: "",
    level: "Intermediate",
  });
}

function removeSkill(index) {
  formData.skills.splice(index, 1);
}

// Certifications
const certificationDialogOpen = ref(false);
const isSavingCertification = ref(false);
const editingCertificationIndex = ref(null);

const certificationForm = ref({
  name: "",
  issuingOrganization: "",
  issueDate: "",
  expirationDate: "",
  credentialId: "",
  credentialUrl: "",
});

function resetCertificationForm() {
  certificationForm.value = {
    name: "",
    issuingOrganization: "",
    issueDate: "",
    expirationDate: "",
    credentialId: "",
    credentialUrl: "",
  };
  editingCertificationIndex.value = null;
}

async function onCertificationSubmit(event) {
  event.preventDefault();
  isSavingCertification.value = true;

  try {
    if (editingCertificationIndex.value !== null) {
      // Update existing certification
      formData.certifications[editingCertificationIndex.value] = {
        ...certificationForm.value,
      };
    } else {
      // Add new certification
      formData.certifications.push({ ...certificationForm.value });
    }

    // Reset form and close dialog
    resetCertificationForm();
    certificationDialogOpen.value = false;
  } catch (error) {
    console.error("Error saving certification:", error);
    alert("Failed to save certification. Please try again.");
  } finally {
    isSavingCertification.value = false;
  }
}

function editCertification(index) {
  const cert = formData.certifications[index];
  certificationForm.value = { ...cert };
  editingCertificationIndex.value = index;
  certificationDialogOpen.value = true;
}

function onCertificationDialogChange(isOpen) {
  certificationDialogOpen.value = isOpen;
  // Reset form when opening dialog for adding (not editing)
  if (isOpen && editingCertificationIndex.value === null) {
    resetCertificationForm();
  }
  // Reset editing state when closing dialog
  if (!isOpen) {
    editingCertificationIndex.value = null;
  }
}

function removeCertification(index) {
  formData.certifications.splice(index, 1);
}

// Publications
const publicationDialogOpen = ref(false);
const isSavingPublication = ref(false);
const editingPublicationIndex = ref(null);

const publicationForm = ref({
  title: "",
  publisher: "",
  publicationDate: "",
  url: "",
});

function resetPublicationForm() {
  publicationForm.value = {
    title: "",
    publisher: "",
    publicationDate: "",
    url: "",
  };
  editingPublicationIndex.value = null;
}

async function onPublicationSubmit(event) {
  event.preventDefault();
  isSavingPublication.value = true;

  try {
    if (editingPublicationIndex.value !== null) {
      // Update existing publication
      formData.publications[editingPublicationIndex.value] = {
        ...publicationForm.value,
      };
    } else {
      // Add new publication
      formData.publications.push({ ...publicationForm.value });
    }

    // Reset form and close dialog
    resetPublicationForm();
    publicationDialogOpen.value = false;
  } catch (error) {
    console.error("Error saving publication:", error);
    alert("Failed to save publication. Please try again.");
  } finally {
    isSavingPublication.value = false;
  }
}

function editPublication(index) {
  const pub = formData.publications[index];
  publicationForm.value = { ...pub };
  editingPublicationIndex.value = index;
  publicationDialogOpen.value = true;
}

function onPublicationDialogChange(isOpen) {
  publicationDialogOpen.value = isOpen;
  // Reset form when opening dialog for adding (not editing)
  if (isOpen && editingPublicationIndex.value === null) {
    resetPublicationForm();
  }
  // Reset editing state when closing dialog
  if (!isOpen) {
    editingPublicationIndex.value = null;
  }
}

function removePublication(index) {
  formData.publications.splice(index, 1);
}

function fillDummyData() {
  // Education
  formData.education = [
    {
      institution: "Stanford University",
      degree: "Master of Science",
      fieldOfStudy: "Computer Science",
      startYear: "2014",
      endYear: "2016",
      grade: "3.9 GPA",
      description:
        "Specialized in Distributed Systems and Machine Learning. Teaching Assistant for CS 101.",
    },
    {
      institution: "University of California, Berkeley",
      degree: "Bachelor of Science",
      fieldOfStudy: "Computer Engineering",
      startYear: "2010",
      endYear: "2014",
      grade: "3.8 GPA",
      description:
        "Dean's List all semesters. President of Computer Science Club.",
    },
  ];

  // Skills
  formData.skills = [
    { name: "JavaScript", level: "Expert" },
    { name: "TypeScript", level: "Expert" },
    { name: "React", level: "Expert" },
    { name: "Node.js", level: "Advanced" },
    { name: "Python", level: "Advanced" },
    { name: "PostgreSQL", level: "Advanced" },
    { name: "AWS", level: "Intermediate" },
    { name: "Docker", level: "Advanced" },
    { name: "GraphQL", level: "Advanced" },
    { name: "MongoDB", level: "Intermediate" },
  ];

  // Certifications
  formData.certifications = [
    {
      name: "AWS Certified Solutions Architect - Professional",
      issuingOrganization: "Amazon Web Services",
      issueDate: "2023-05",
      expirationDate: "2026-05",
      credentialId: "AWS-PSA-123456",
      credentialUrl: "https://aws.amazon.com/verification",
    },
    {
      name: "MongoDB Certified Developer",
      issuingOrganization: "MongoDB Inc.",
      issueDate: "2022-09",
      expirationDate: "",
      credentialId: "MONGO-DEV-789012",
      credentialUrl: "https://university.mongodb.com/certification",
    },
    {
      name: "Professional Scrum Master I",
      issuingOrganization: "Scrum.org",
      issueDate: "2021-03",
      expirationDate: "",
      credentialId: "PSM-I-345678",
      credentialUrl: "https://scrum.org/certificates",
    },
  ];

  // Publications
  formData.publications = [
    {
      title: "Optimizing Microservices Performance in Cloud Environments",
      publisher: "IEEE Software",
      publicationDate: "2023-11",
      url: "https://ieeexplore.ieee.org/document/example",
    },
    {
      title: "Best Practices for React Application Architecture",
      publisher: "Medium Engineering Blog",
      publicationDate: "2023-06",
      url: "https://medium.com/engineering/react-architecture",
    },
  ];
}

// Helper function to format month-year dates
function formatMonthYear(dateString) {
  if (!dateString) return "";
  const [year, month] = dateString.split("-");
  const date = new Date(year, month - 1);
  return date.toLocaleDateString("en-US", { year: "numeric", month: "short" });
}
</script>

<style scoped>
.step-content {
  max-width: 900px;
  margin: 0 auto;
}

.step-header-actions {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  gap: 20px;
}

.dummy-data-btn {
  flex-shrink: 0;
}

.dummy-data-btn .icon {
  margin-right: 8px;
}

.step-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.step-description {
  font-size: 16px;
  color: #64748b;
  margin: 0 0 32px 0;
}

.form-card {
  margin-bottom: 32px;
}

.section-card {
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  transition: box-shadow 0.2s ease;
}

.section-card:hover {
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
}

.section-title-with-icon {
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-icon {
  color: #3b82f6;
  flex-shrink: 0;
}

.form-section-title {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-item-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-weight: 500;
  font-size: 14px;
  border-radius: 8px;
  border: 1.5px solid #e5e7eb;
  background: white;
  color: #0f172a;
  transition: all 0.2s ease;
}

.add-item-btn:hover {
  border-color: #0f172a;
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.add-item-btn:active {
  transform: translateY(0);
  box-shadow: none;
}

.btn-icon {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.add-item-btn:hover .btn-icon {
  transform: rotate(90deg);
}

.repeatable-item {
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 12px;
  position: relative;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.item-number {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
  align-items: flex-end;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #0f172a;
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.15s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
}

.form-group textarea {
  resize: vertical;
}

.remove-btn {
  color: #ef4444;
  flex-shrink: 0;
}

/* Education List */
.education-list {
  margin-top: 20px;
}

.education-item {
  padding: 16px 0;
}

.education-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.education-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.education-institution {
  font-size: 15px;
  font-weight: 500;
  color: #3b82f6;
  margin: 0 0 4px 0;
}

.education-meta {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 8px 0;
}

.education-description {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  margin: 8px 0 0 0;
}

.education-divider {
  margin: 20px 0 0 0;
  border: none;
  border-top: 1px solid #e5e7eb;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.action-buttons {
  display: flex;
  gap: 4px;
}

.edit-btn {
  color: #3b82f6;
  padding: 8px;
  height: auto;
}

.edit-btn:hover {
  background: #dbeafe;
  color: #2563eb;
}

.delete-btn {
  color: #ef4444;
  padding: 8px;
  height: auto;
}

.delete-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #64748b;
  font-size: 14px;
}

/* Skills */
.skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 20px;
}

.skill-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background-color: #eff6ff;
  color: #1e40af;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid #dbeafe;
  transition: all 0.2s;
}

.skill-badge:hover {
  background-color: #dbeafe;
  border-color: #bfdbfe;
}

.skill-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2px;
  background: none;
  border: none;
  cursor: pointer;
  color: #3b82f6;
  border-radius: 3px;
  transition: all 0.2s;
}

.skill-remove:hover {
  background-color: #3b82f6;
  color: white;
}

/* Dialog Form */
.dialog-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 0;
}

.dialog-form .form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

/* Certifications */
.certifications-list {
  margin-top: 20px;
}

.certification-item {
  padding: 16px 0;
}

.certification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.certification-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.certification-organization {
  font-size: 15px;
  font-weight: 500;
  color: #3b82f6;
  margin: 0 0 4px 0;
}

.certification-meta {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 4px 0;
}

.certification-credential {
  font-size: 13px;
  color: #64748b;
  margin: 4px 0;
}

.certification-url {
  font-size: 13px;
  margin: 8px 0 0 0;
}

.certification-url a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.certification-url a:hover {
  color: #2563eb;
  text-decoration: underline;
}

.certification-divider {
  margin: 20px 0 0 0;
  border: none;
  border-top: 1px solid #e5e7eb;
}

/* Publications */
.publications-list {
  margin-top: 20px;
}

.publication-item {
  padding: 16px 0;
}

.publication-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.publication-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.publication-publisher {
  font-size: 15px;
  font-weight: 500;
  color: #3b82f6;
  margin: 0 0 4px 0;
}

.publication-meta {
  font-size: 13px;
  color: #64748b;
  margin: 4px 0;
}

.publication-url {
  font-size: 13px;
  margin: 8px 0 0 0;
}

.publication-url a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.publication-url a:hover {
  color: #2563eb;
  text-decoration: underline;
}

.publication-divider {
  margin: 20px 0 0 0;
  border: none;
  border-top: 1px solid #e5e7eb;
}
</style>
