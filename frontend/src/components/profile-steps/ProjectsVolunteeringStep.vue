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
    <Card class="form-card section-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Projects</h3>
          <Dialog
            :open="projectDialogOpen"
            @update:open="onProjectDialogChange"
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
                Add Project
              </Button>
            </DialogTrigger>
            <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>{{
                  editingProjectIndex !== null ? "Edit Project" : "Add Project"
                }}</DialogTitle>
                <DialogDescription>
                  {{
                    editingProjectIndex !== null
                      ? "Update your project details."
                      : "Add your project details."
                  }}
                </DialogDescription>
              </DialogHeader>
              <form @submit="onProjectSubmit" class="dialog-form">
                <div class="form-group">
                  <label>Project Title <span class="required">*</span></label>
                  <input
                    v-model="projectForm.title"
                    type="text"
                    required
                    placeholder="E-commerce Platform"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                </div>

                <div class="form-group">
                  <label>Role</label>
                  <input
                    v-model="projectForm.role"
                    type="text"
                    placeholder="Lead Developer"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                </div>

                <div class="form-group">
                  <label>Description</label>
                  <textarea
                    v-model="projectForm.description"
                    rows="4"
                    placeholder="Describe the project, your contributions, and the impact..."
                    class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  ></textarea>
                </div>

                <div class="form-group">
                  <label>Technologies Used</label>
                  <input
                    v-model="projectForm.technologiesText"
                    type="text"
                    placeholder="React, Node.js, MongoDB, AWS"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                  <small class="help-text">Separate with commas</small>
                </div>

                <div class="form-group">
                  <label>Project Link</label>
                  <input
                    v-model="projectForm.link"
                    type="url"
                    placeholder="https://github.com/username/project"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                </div>

                <DialogFooter>
                  <Button
                    @click="projectDialogOpen = false"
                    variant="outline"
                    type="button"
                    :disabled="isSavingProject"
                  >
                    Cancel
                  </Button>
                  <Button type="submit" :disabled="isSavingProject">
                    {{
                      isSavingProject
                        ? "Saving..."
                        : editingProjectIndex !== null
                        ? "Update Project"
                        : "Add Project"
                    }}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <!-- Projects List -->
        <div v-if="formData.projects.length > 0" class="projects-list">
          <div
            v-for="(project, index) in formData.projects"
            :key="index"
            class="project-item"
          >
            <div class="project-header">
              <h3 class="project-title">{{ project.title }}</h3>
              <div class="action-buttons">
                <Button
                  @click="editProject(index)"
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
                  @click="removeProject(index)"
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
            <p v-if="project.role" class="project-role">{{ project.role }}</p>
            <p v-if="project.description" class="project-description">
              {{ project.description }}
            </p>
            <div
              v-if="project.technologies && project.technologies.length > 0"
              class="project-technologies"
            >
              <span
                v-for="(tech, techIndex) in project.technologies"
                :key="techIndex"
                class="tech-badge"
              >
                {{ tech }}
              </span>
            </div>
            <p v-if="project.link" class="project-link">
              <a :href="project.link" target="_blank" rel="noopener noreferrer">
                View Project
              </a>
            </p>
            <hr
              v-if="index < formData.projects.length - 1"
              class="project-divider"
            />
          </div>
        </div>

        <div v-else class="empty-state">
          <p>No projects added yet. Click "Add Project" to get started.</p>
        </div>
      </CardContent>
    </Card>

    <!-- Volunteering -->
    <Card class="form-card section-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Volunteering</h3>
          <Dialog
            :open="volunteeringDialogOpen"
            @update:open="onVolunteeringDialogChange"
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
                Add Volunteering
              </Button>
            </DialogTrigger>
            <DialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>{{
                  editingVolunteeringIndex !== null
                    ? "Edit Volunteering"
                    : "Add Volunteering"
                }}</DialogTitle>
                <DialogDescription>
                  {{
                    editingVolunteeringIndex !== null
                      ? "Update your volunteering experience."
                      : "Add your volunteering experience."
                  }}
                </DialogDescription>
              </DialogHeader>
              <form @submit="onVolunteeringSubmit" class="dialog-form">
                <div class="form-row">
                  <div class="form-group">
                    <label>Organization <span class="required">*</span></label>
                    <input
                      v-model="volunteeringForm.organization"
                      type="text"
                      required
                      placeholder="Red Cross"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>

                  <div class="form-group">
                    <label>Role</label>
                    <input
                      v-model="volunteeringForm.role"
                      type="text"
                      placeholder="Volunteer Coordinator"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>Start Date</label>
                    <input
                      v-model="volunteeringForm.startDate"
                      type="month"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>

                  <div class="form-group">
                    <label>End Date</label>
                    <input
                      v-model="volunteeringForm.endDate"
                      type="month"
                      placeholder="Leave empty if ongoing"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    />
                  </div>
                </div>

                <div class="form-group">
                  <label>Description</label>
                  <textarea
                    v-model="volunteeringForm.description"
                    rows="3"
                    placeholder="Describe your volunteer work and contributions..."
                    class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  ></textarea>
                </div>

                <DialogFooter>
                  <Button
                    @click="volunteeringDialogOpen = false"
                    variant="outline"
                    type="button"
                    :disabled="isSavingVolunteering"
                  >
                    Cancel
                  </Button>
                  <Button type="submit" :disabled="isSavingVolunteering">
                    {{
                      isSavingVolunteering
                        ? "Saving..."
                        : editingVolunteeringIndex !== null
                        ? "Update Volunteering"
                        : "Add Volunteering"
                    }}
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <!-- Volunteering List -->
        <div v-if="formData.volunteering.length > 0" class="volunteering-list">
          <div
            v-for="(vol, index) in formData.volunteering"
            :key="index"
            class="volunteering-item"
          >
            <div class="volunteering-header">
              <h3 class="volunteering-title">{{ vol.organization }}</h3>
              <div class="action-buttons">
                <Button
                  @click="editVolunteering(index)"
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
                  @click="removeVolunteering(index)"
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
            <p v-if="vol.role" class="volunteering-role">{{ vol.role }}</p>
            <p v-if="vol.startDate || vol.endDate" class="volunteering-dates">
              <span v-if="vol.startDate">{{
                formatMonthYear(vol.startDate)
              }}</span>
              <span v-if="vol.startDate && vol.endDate"> - </span>
              <span v-if="vol.endDate">{{ formatMonthYear(vol.endDate) }}</span>
              <span v-if="vol.startDate && !vol.endDate"> - Present</span>
            </p>
            <p v-if="vol.description" class="volunteering-description">
              {{ vol.description }}
            </p>
            <hr
              v-if="index < formData.volunteering.length - 1"
              class="volunteering-divider"
            />
          </div>
        </div>

        <div v-else class="empty-state">
          <p>
            No volunteering experience added yet. Click "Add Volunteering" to
            get started.
          </p>
        </div>
      </CardContent>
    </Card>

    <!-- Job Preferences (Optional) -->
    <Card class="form-card section-card">
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
import { defineProps, defineEmits, ref } from "vue";
import { useAuth } from "@clerk/vue";
import { updateMasterProfile } from "@/services/api";
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

const auth = useAuth();

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue"]);

const formData = props.modelValue;

// Projects
const projectDialogOpen = ref(false);
const isSavingProject = ref(false);
const editingProjectIndex = ref(null);

const projectForm = ref({
  title: "",
  description: "",
  role: "",
  technologies: [],
  technologiesText: "",
  link: "",
});

function resetProjectForm() {
  projectForm.value = {
    title: "",
    description: "",
    role: "",
    technologies: [],
    technologiesText: "",
    link: "",
  };
  editingProjectIndex.value = null;
}

async function onProjectSubmit(event) {
  event.preventDefault();
  isSavingProject.value = true;

  try {
    // Parse technologies from text
    const technologies = projectForm.value.technologiesText
      .split(",")
      .map((tech) => tech.trim())
      .filter((tech) => tech.length > 0);

    const projectData = {
      title: projectForm.value.title,
      description: projectForm.value.description,
      role: projectForm.value.role,
      technologies,
      link: projectForm.value.link,
    };

    if (editingProjectIndex.value !== null) {
      // Update existing project
      console.log("[ProjectsVolunteeringStep] Updating project");
      formData.projects[editingProjectIndex.value] = projectData;
    } else {
      // Add new project
      console.log("[ProjectsVolunteeringStep] Adding new project");
      formData.projects.push(projectData);
    }

    // Save to database immediately
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        projects: formData.projects,
      });
      console.log("[ProjectsVolunteeringStep] Project saved to database");
    }

    // Reset form and close dialog
    resetProjectForm();
    projectDialogOpen.value = false;
  } catch (error) {
    console.error("[ProjectsVolunteeringStep] Error saving project:", error);
    alert("Failed to save project. Please try again.");
  } finally {
    isSavingProject.value = false;
  }
}

function editProject(index) {
  const project = formData.projects[index];
  projectForm.value = { ...project };
  editingProjectIndex.value = index;
  projectDialogOpen.value = true;
}

function onProjectDialogChange(isOpen) {
  projectDialogOpen.value = isOpen;
  // Reset form when opening dialog for adding (not editing)
  if (isOpen && editingProjectIndex.value === null) {
    resetProjectForm();
  }
  // Reset editing state when closing dialog
  if (!isOpen) {
    editingProjectIndex.value = null;
  }
}

async function removeProject(index) {
  const removedProject = formData.projects[index];

  // Remove from local state
  formData.projects.splice(index, 1);

  try {
    // Save to database immediately
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        projects: formData.projects,
      });
      console.log(
        "[ProjectsVolunteeringStep] Project removed and saved to database"
      );
    }
  } catch (error) {
    console.error(
      "[ProjectsVolunteeringStep] Failed to remove project:",
      error
    );
    // Restore the project if save failed
    formData.projects.splice(index, 0, removedProject);
    alert("Failed to remove project. Please try again.");
  }
}

// Volunteering
const volunteeringDialogOpen = ref(false);
const isSavingVolunteering = ref(false);
const editingVolunteeringIndex = ref(null);

const volunteeringForm = ref({
  organization: "",
  role: "",
  startDate: "",
  endDate: "",
  description: "",
});

function resetVolunteeringForm() {
  volunteeringForm.value = {
    organization: "",
    role: "",
    startDate: "",
    endDate: "",
    description: "",
  };
  editingVolunteeringIndex.value = null;
}

async function onVolunteeringSubmit(event) {
  event.preventDefault();
  isSavingVolunteering.value = true;

  try {
    const volunteeringData = {
      organization: volunteeringForm.value.organization,
      role: volunteeringForm.value.role,
      startDate: volunteeringForm.value.startDate,
      endDate: volunteeringForm.value.endDate,
      description: volunteeringForm.value.description,
    };

    if (editingVolunteeringIndex.value !== null) {
      // Update existing volunteering
      console.log("[ProjectsVolunteeringStep] Updating volunteering");
      formData.volunteering[editingVolunteeringIndex.value] = volunteeringData;
    } else {
      // Add new volunteering
      console.log("[ProjectsVolunteeringStep] Adding new volunteering");
      formData.volunteering.push(volunteeringData);
    }

    // Save to database immediately
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        volunteering: formData.volunteering,
      });
      console.log("[ProjectsVolunteeringStep] Volunteering saved to database");
    }

    // Reset form and close dialog
    resetVolunteeringForm();
    volunteeringDialogOpen.value = false;
  } catch (error) {
    console.error(
      "[ProjectsVolunteeringStep] Error saving volunteering:",
      error
    );
    alert("Failed to save volunteering. Please try again.");
  } finally {
    isSavingVolunteering.value = false;
  }
}

function editVolunteering(index) {
  const vol = formData.volunteering[index];
  volunteeringForm.value = { ...vol };
  editingVolunteeringIndex.value = index;
  volunteeringDialogOpen.value = true;
}

function onVolunteeringDialogChange(isOpen) {
  volunteeringDialogOpen.value = isOpen;
  // Reset form when opening dialog for adding (not editing)
  if (isOpen && editingVolunteeringIndex.value === null) {
    resetVolunteeringForm();
  }
  // Reset editing state when closing dialog
  if (!isOpen) {
    editingVolunteeringIndex.value = null;
  }
}

async function removeVolunteering(index) {
  const removedVolunteering = formData.volunteering[index];

  // Remove from local state
  formData.volunteering.splice(index, 1);

  try {
    // Save to database immediately
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        volunteering: formData.volunteering,
      });
      console.log(
        "[ProjectsVolunteeringStep] Volunteering removed and saved to database"
      );
    }
  } catch (error) {
    console.error(
      "[ProjectsVolunteeringStep] Failed to remove volunteering:",
      error
    );
    // Restore the volunteering if save failed
    formData.volunteering.splice(index, 0, removedVolunteering);
    alert("Failed to remove volunteering. Please try again.");
  }
}

// Helper function to format month-year dates
function formatMonthYear(dateString) {
  if (!dateString) return "";
  const [year, month] = dateString.split("-");
  const date = new Date(year, month - 1);
  return date.toLocaleDateString("en-US", { year: "numeric", month: "short" });
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

async function fillDummyData() {
  try {
    console.log("[ProjectsVolunteeringStep] Filling with test data");

    const dummyProjects = [
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
        technologies: [
          "Python",
          "TensorFlow",
          "FastAPI",
          "PostgreSQL",
          "Docker",
        ],
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

    const dummyVolunteering = [
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

    const dummyJobPreferences = {
      desiredRoles: [
        "Senior Full-Stack Developer",
        "Tech Lead",
        "Engineering Manager",
        "Solutions Architect",
      ],
      employmentTypes: ["Full-time", "Contract"],
      locations: ["San Francisco, CA", "Remote", "New York, NY", "Seattle, WA"],
      openToRelocation: true,
    };

    // Save directly to database
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        projects: dummyProjects,
        volunteering: dummyVolunteering,
        jobPreferences: dummyJobPreferences,
      });
      console.log("[ProjectsVolunteeringStep] Test data saved to database");

      // Update local state to reflect saved data
      formData.projects = dummyProjects;
      formData.volunteering = dummyVolunteering;

      // Update job preferences with text fields for UI
      formData.jobPreferences.desiredRolesText =
        "Senior Full-Stack Developer, Tech Lead, Engineering Manager, Solutions Architect";
      formData.jobPreferences.desiredRoles = dummyJobPreferences.desiredRoles;
      formData.jobPreferences.employmentTypesText = "Full-time, Contract";
      formData.jobPreferences.employmentTypes =
        dummyJobPreferences.employmentTypes;
      formData.jobPreferences.locationsText =
        "San Francisco, CA, Remote, New York, NY, Seattle, WA";
      formData.jobPreferences.locations = dummyJobPreferences.locations;
      formData.jobPreferences.openToRelocation =
        dummyJobPreferences.openToRelocation;

      alert("Test data filled and saved successfully!");
    }
  } catch (error) {
    console.error("[ProjectsVolunteeringStep] Error filling test data:", error);
    alert("Failed to fill test data. Please try again.");
  }
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.step-description {
  font-size: 16px;
  color: #64748b;
  margin: 0 0 32px 0;
  line-height: 1.6;
}

.form-card {
  margin-bottom: 32px;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
}

.form-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
  transform: translateY(-2px);
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
  color: #667eea;
  flex-shrink: 0;
}

.form-section-title {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-section-title::before {
  content: "";
  width: 4px;
  height: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
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
  padding: 10px 20px;
  font-weight: 600;
  font-size: 14px;
  border-radius: 8px;
  background: white;
  color: #667eea;
  border: 2px solid transparent;
  background-image: linear-gradient(white, white),
    linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
}

.add-item-btn:hover {
  background-image: linear-gradient(135deg, #f8f9ff 0%, #faf8ff 100%),
    linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
  color: #5568d3;
}

.add-item-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
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
  font-size: 14px;
}

/* Projects List */
.projects-list {
  margin-top: 20px;
}

.project-item {
  padding: 16px 0;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.project-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.project-role {
  font-size: 15px;
  font-weight: 500;
  color: #3b82f6;
  margin: 0 0 8px 0;
}

.project-description {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  margin: 8px 0;
}

.project-technologies {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0;
}

.tech-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  background-color: #eff6ff;
  color: #1e40af;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid #dbeafe;
}

.project-link {
  font-size: 13px;
  margin: 8px 0 0 0;
}

.project-link a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.project-link a:hover {
  color: #2563eb;
  text-decoration: underline;
}

.project-divider {
  margin: 20px 0 0 0;
  border: none;
  border-top: 1px solid #e5e7eb;
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

/* Dialog Form */
.dialog-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 0;
}

.dialog-form button[type="submit"] {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
}

.dialog-form button[type="submit"]:hover {
  background: linear-gradient(135deg, #5568d3 0%, #653a8a 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
}

.dialog-form button[variant="outline"] {
  background: white;
  color: #667eea;
  border: 2px solid transparent;
  background-image: linear-gradient(white, white),
    linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  font-weight: 500;
  transition: all 0.3s ease;
}

.dialog-form button[variant="outline"]:hover {
  background-image: linear-gradient(135deg, #f8f9ff 0%, #faf8ff 100%),
    linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translateY(-2px);
  color: #5568d3;
}

.dialog-form .form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* Volunteering List */
.volunteering-list {
  margin-top: 20px;
}

.volunteering-item {
  padding: 16px 0;
}

.volunteering-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.volunteering-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.volunteering-role {
  font-size: 15px;
  font-weight: 500;
  color: #3b82f6;
  margin: 0 0 4px 0;
}

.volunteering-dates {
  font-size: 13px;
  color: #64748b;
  margin: 0 0 8px 0;
}

.volunteering-description {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  margin: 8px 0 0 0;
}

.volunteering-divider {
  margin: 20px 0 0 0;
  border: none;
  border-top: 1px solid #e5e7eb;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
