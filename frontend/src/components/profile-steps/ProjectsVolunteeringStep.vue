<template>
  <div class="step-content">
    <div class="step-header-actions">
      <div>
        <h2 class="step-title">Projects & Volunteering</h2>
        <p class="step-description">
          Showcase your personal projects and volunteer work
        </p>
      </div>
      <Button @click="fillDummyData" variant="outline" class="dummy-data-btn">
        <span class="icon">✨</span>
        Fill with Test Data
      </Button>
    </div>

    <!-- Projects -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Projects</h3>
          <Button @click="addProject" size="sm" variant="outline">
            + Add Project
          </Button>
        </div>

        <div
          v-for="(project, index) in formData.projects"
          :key="index"
          class="repeatable-item"
        >
          <div class="item-header">
            <span class="item-number">Project {{ index + 1 }}</span>
            <Button
              @click="removeProject(index)"
              size="sm"
              variant="ghost"
              class="remove-btn"
            >
              ✕
            </Button>
          </div>

          <div class="form-group">
            <label>Project Title</label>
            <input
              v-model="project.title"
              type="text"
              placeholder="E-commerce Platform"
            />
          </div>

          <div class="form-group">
            <label>Role</label>
            <input
              v-model="project.role"
              type="text"
              placeholder="Lead Developer"
            />
          </div>

          <div class="form-group">
            <label>Description</label>
            <textarea
              v-model="project.description"
              rows="4"
              placeholder="Describe the project, your contributions, and the impact..."
            ></textarea>
          </div>

          <div class="form-group">
            <label>Technologies Used</label>
            <input
              v-model="project.technologiesText"
              type="text"
              placeholder="React, Node.js, MongoDB, AWS"
              @input="updateTechnologies(project)"
            />
            <small class="help-text">Separate with commas</small>
          </div>

          <div class="form-group">
            <label>Project Link</label>
            <input
              v-model="project.link"
              type="url"
              placeholder="https://github.com/username/project"
            />
          </div>
        </div>

        <div v-if="formData.projects.length === 0" class="empty-state">
          <p>No projects added yet.</p>
        </div>
      </CardContent>
    </Card>

    <!-- Volunteering -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Volunteering</h3>
          <Button @click="addVolunteering" size="sm" variant="outline">
            + Add Volunteering
          </Button>
        </div>

        <div
          v-for="(vol, index) in formData.volunteering"
          :key="index"
          class="repeatable-item"
        >
          <div class="item-header">
            <span class="item-number">Volunteer {{ index + 1 }}</span>
            <Button
              @click="removeVolunteering(index)"
              size="sm"
              variant="ghost"
              class="remove-btn"
            >
              ✕
            </Button>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Organization</label>
              <input
                v-model="vol.organization"
                type="text"
                placeholder="Red Cross"
              />
            </div>

            <div class="form-group">
              <label>Role</label>
              <input
                v-model="vol.role"
                type="text"
                placeholder="Volunteer Coordinator"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Start Date</label>
              <input v-model="vol.startDate" type="month" />
            </div>

            <div class="form-group">
              <label>End Date</label>
              <input
                v-model="vol.endDate"
                type="month"
                placeholder="Leave empty if ongoing"
              />
            </div>
          </div>

          <div class="form-group">
            <label>Description</label>
            <textarea
              v-model="vol.description"
              rows="3"
              placeholder="Describe your volunteer work and contributions..."
            ></textarea>
          </div>
        </div>

        <div v-if="formData.volunteering.length === 0" class="empty-state">
          <p>No volunteering experience added yet.</p>
        </div>
      </CardContent>
    </Card>

    <!-- Job Preferences (Optional) -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <h3 class="form-section-title">Job Preferences (Optional)</h3>

        <div class="form-group">
          <label>Desired Roles</label>
          <input
            v-model="formData.jobPreferences.desiredRolesText"
            type="text"
            placeholder="Software Engineer, Full-Stack Developer"
            @input="updateDesiredRoles"
          />
          <small class="help-text">Separate with commas</small>
        </div>

        <div class="form-group">
          <label>Preferred Employment Types</label>
          <input
            v-model="formData.jobPreferences.employmentTypesText"
            type="text"
            placeholder="Full-time, Remote, Contract"
            @input="updateEmploymentTypes"
          />
          <small class="help-text">Separate with commas</small>
        </div>

        <div class="form-group">
          <label>Preferred Locations</label>
          <input
            v-model="formData.jobPreferences.locationsText"
            type="text"
            placeholder="San Francisco, New York, Remote"
            @input="updateLocations"
          />
          <small class="help-text">Separate with commas</small>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              v-model="formData.jobPreferences.openToRelocation"
              type="checkbox"
            />
            <span>Open to relocation</span>
          </label>
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

// Projects
function addProject() {
  formData.projects.push({
    title: "",
    description: "",
    role: "",
    technologies: [],
    technologiesText: "",
    link: "",
  });
}

function removeProject(index) {
  formData.projects.splice(index, 1);
}

function updateTechnologies(project) {
  project.technologies = project.technologiesText
    .split(",")
    .map((tech) => tech.trim())
    .filter((tech) => tech.length > 0);
}

// Volunteering
function addVolunteering() {
  formData.volunteering.push({
    organization: "",
    role: "",
    startDate: "",
    endDate: "",
    description: "",
  });
}

function removeVolunteering(index) {
  formData.volunteering.splice(index, 1);
}

// Job Preferences
function updateDesiredRoles() {
  formData.jobPreferences.desiredRoles =
    formData.jobPreferences.desiredRolesText
      .split(",")
      .map((role) => role.trim())
      .filter((role) => role.length > 0);
}

function updateEmploymentTypes() {
  formData.jobPreferences.employmentTypes =
    formData.jobPreferences.employmentTypesText
      .split(",")
      .map((type) => type.trim())
      .filter((type) => type.length > 0);
}

function updateLocations() {
  formData.jobPreferences.locations = formData.jobPreferences.locationsText
    .split(",")
    .map((loc) => loc.trim())
    .filter((loc) => loc.length > 0);
}

function fillDummyData() {
  // Projects
  formData.projects = [
    {
      title: "DevCollab - Real-time Collaboration Platform",
      description:
        "Built a real-time code collaboration platform with video chat, shared coding environment, and version control integration. Implemented WebSocket connections for real-time synchronization and WebRTC for video communication.",
      role: "Full-Stack Developer & Co-founder",
      technologiesText:
        "React, Node.js, Socket.io, WebRTC, MongoDB, Redis, AWS",
      technologies: [
        "React",
        "Node.js",
        "Socket.io",
        "WebRTC",
        "MongoDB",
        "Redis",
        "AWS",
      ],
      link: "https://devcollab.io",
    },
    {
      title: "AITaskOptimizer - Machine Learning Task Scheduler",
      description:
        "Developed an intelligent task scheduling system using machine learning to predict task completion times and optimize resource allocation. Achieved 35% improvement in task throughput.",
      role: "Lead Developer",
      technologiesText: "Python, TensorFlow, FastAPI, PostgreSQL, Docker",
      technologies: ["Python", "TensorFlow", "FastAPI", "PostgreSQL", "Docker"],
      link: "https://github.com/sarahchen/ai-task-optimizer",
    },
    {
      title: "OpenSourceContrib - Contribution Tracker",
      description:
        "Created an open-source contribution tracking tool that aggregates GitHub activity and provides insights on contribution patterns. Used by 500+ developers.",
      role: "Creator & Maintainer",
      technologiesText: "TypeScript, Next.js, GraphQL, GitHub API, Vercel",
      technologies: [
        "TypeScript",
        "Next.js",
        "GraphQL",
        "GitHub API",
        "Vercel",
      ],
      link: "https://opensourcecontrib.com",
    },
  ];

  // Volunteering
  formData.volunteering = [
    {
      organization: "Code for Good",
      role: "Volunteer Developer",
      startDate: "2021-01",
      endDate: "",
      description:
        "Contribute to open-source projects benefiting non-profit organizations. Led development of a donation management system for local food banks.",
    },
    {
      organization: "Girls Who Code",
      role: "Mentor & Workshop Facilitator",
      startDate: "2020-06",
      endDate: "2023-12",
      description:
        "Mentored high school students in web development fundamentals. Conducted monthly workshops on JavaScript, React, and career guidance in tech.",
    },
  ];

  // Job Preferences
  formData.jobPreferences.desiredRolesText =
    "Senior Full-Stack Developer, Tech Lead, Engineering Manager, Solutions Architect";
  formData.jobPreferences.desiredRoles = [
    "Senior Full-Stack Developer",
    "Tech Lead",
    "Engineering Manager",
    "Solutions Architect",
  ];

  formData.jobPreferences.employmentTypesText = "Full-time, Contract";
  formData.jobPreferences.employmentTypes = ["Full-time", "Contract"];

  formData.jobPreferences.locationsText =
    "San Francisco, CA, Remote, New York, NY, Seattle, WA";
  formData.jobPreferences.locations = [
    "San Francisco, CA",
    "Remote",
    "New York, NY",
    "Seattle, WA",
  ];

  formData.jobPreferences.openToRelocation = true;
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
  margin: 0 0 20px 0;
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
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
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

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.help-text {
  font-size: 12px;
  color: #64748b;
}

.remove-btn {
  color: #ef4444;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #64748b;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
