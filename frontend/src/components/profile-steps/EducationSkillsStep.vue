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
          <Button @click="addEducation" size="sm" variant="outline">
            + Add Education
          </Button>
        </div>

        <div
          v-for="(edu, index) in formData.education"
          :key="index"
          class="repeatable-item"
        >
          <div class="item-header">
            <span class="item-number">{{ index + 1 }}</span>
            <Button
              @click="removeEducation(index)"
              size="sm"
              variant="ghost"
              class="remove-btn"
            >
              ✕
            </Button>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Institution <span class="required">*</span></label>
              <input
                v-model="edu.institution"
                type="text"
                required
                placeholder="Stanford University"
              />
            </div>

            <div class="form-group">
              <label>Degree <span class="required">*</span></label>
              <input
                v-model="edu.degree"
                type="text"
                required
                placeholder="Bachelor of Science"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Field of Study</label>
              <input
                v-model="edu.fieldOfStudy"
                type="text"
                placeholder="Computer Science"
              />
            </div>

            <div class="form-group">
              <label>Grade/GPA</label>
              <input v-model="edu.grade" type="text" placeholder="3.8/4.0" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Start Year</label>
              <input v-model="edu.startYear" type="text" placeholder="2014" />
            </div>

            <div class="form-group">
              <label>End Year</label>
              <input v-model="edu.endYear" type="text" placeholder="2018" />
            </div>
          </div>

          <div class="form-group">
            <label>Description</label>
            <textarea
              v-model="edu.description"
              rows="2"
              placeholder="Relevant coursework, honors, activities..."
            ></textarea>
          </div>
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
import { defineProps, defineEmits } from "vue";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue"]);

const formData = props.modelValue;

// Education
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

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
