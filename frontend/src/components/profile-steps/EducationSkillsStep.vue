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
    <Card class="form-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Education</h3>
          <Dialog
            :open="educationDialogOpen"
            @update:open="onEducationDialogChange"
          >
            <DialogTrigger>
              <Button size="sm" variant="outline"> + Add Education </Button>
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
          <Card
            v-for="(edu, index) in formData.education"
            :key="index"
            class="education-card"
          >
            <CardContent class="pt-6">
              <div class="card-header">
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
            </CardContent>
          </Card>
        </div>

        <div v-else class="empty-state">
          <p>No education added yet. Click "Add Education" to get started.</p>
        </div>
      </CardContent>
    </Card>

    <!-- Skills -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Skills</h3>
          <Button @click="addSkill" size="sm" variant="outline">
            + Add Skill
          </Button>
        </div>

        <div
          v-for="(skill, index) in formData.skills"
          :key="index"
          class="repeatable-item"
        >
          <div class="form-row">
            <div class="form-group">
              <label>Skill Name</label>
              <input
                v-model="skill.name"
                type="text"
                placeholder="JavaScript"
              />
            </div>

            <div class="form-group">
              <label>Proficiency Level</label>
              <select v-model="skill.level">
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
                <option value="Expert">Expert</option>
              </select>
            </div>

            <Button
              @click="removeSkill(index)"
              size="sm"
              variant="ghost"
              class="remove-btn"
            >
              ✕
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Certifications -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Certifications</h3>
          <Button @click="addCertification" size="sm" variant="outline">
            + Add Certification
          </Button>
        </div>

        <div
          v-for="(cert, index) in formData.certifications"
          :key="index"
          class="repeatable-item"
        >
          <div class="item-header">
            <span class="item-number">{{ index + 1 }}</span>
            <Button
              @click="removeCertification(index)"
              size="sm"
              variant="ghost"
              class="remove-btn"
            >
              ✕
            </Button>
          </div>

          <div class="form-group">
            <label>Certification Name</label>
            <input
              v-model="cert.name"
              type="text"
              placeholder="AWS Certified Solutions Architect"
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Issuing Organization</label>
              <input
                v-model="cert.issuingOrganization"
                type="text"
                placeholder="Amazon Web Services"
              />
            </div>

            <div class="form-group">
              <label>Issue Date</label>
              <input v-model="cert.issueDate" type="month" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Expiration Date</label>
              <input v-model="cert.expirationDate" type="month" />
            </div>

            <div class="form-group">
              <label>Credential ID</label>
              <input
                v-model="cert.credentialId"
                type="text"
                placeholder="ABC123XYZ"
              />
            </div>
          </div>

          <div class="form-group">
            <label>Credential URL</label>
            <input
              v-model="cert.credentialUrl"
              type="url"
              placeholder="https://..."
            />
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Publications -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Publications</h3>
          <Button @click="addPublication" size="sm" variant="outline">
            + Add Publication
          </Button>
        </div>

        <div
          v-for="(pub, index) in formData.publications"
          :key="index"
          class="repeatable-item"
        >
          <div class="item-header">
            <span class="item-number">{{ index + 1 }}</span>
            <Button
              @click="removePublication(index)"
              size="sm"
              variant="ghost"
              class="remove-btn"
            >
              ✕
            </Button>
          </div>

          <div class="form-group">
            <label>Title</label>
            <input
              v-model="pub.title"
              type="text"
              placeholder="Research Paper Title"
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Publisher</label>
              <input
                v-model="pub.publisher"
                type="text"
                placeholder="IEEE, ACM, etc."
              />
            </div>

            <div class="form-group">
              <label>Publication Date</label>
              <input v-model="pub.publicationDate" type="month" />
            </div>
          </div>

          <div class="form-group">
            <label>URL</label>
            <input v-model="pub.url" type="url" placeholder="https://..." />
          </div>
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
function addCertification() {
  formData.certifications.push({
    name: "",
    issuingOrganization: "",
    issueDate: "",
    expirationDate: "",
    credentialId: "",
    credentialUrl: "",
  });
}

function removeCertification(index) {
  formData.certifications.splice(index, 1);
}

// Publications
function addPublication() {
  formData.publications.push({
    title: "",
    publisher: "",
    publicationDate: "",
    url: "",
  });
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
  margin-bottom: 24px;
}

.form-section-title {
  font-size: 18px;
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
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 20px;
}

.education-card {
  border: 1px solid #e5e7eb;
  transition: border-color 0.2s ease;
}

.education-card:hover {
  border-color: #d1d5db;
}

.card-header {
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
</style>
