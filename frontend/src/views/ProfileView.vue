<template>
  <div class="profile-view">
    <div class="page-header">
      <h1>Master Profile</h1>
      <p class="page-description">
        Build your comprehensive professional profile step by step
      </p>
    </div>

    <!-- Breadcrumb Navigation -->
    <Breadcrumb class="breadcrumb-wrapper">
      <BreadcrumbList>
        <BreadcrumbItem v-for="(step, index) in steps" :key="index">
          <BreadcrumbLink
            v-if="index < currentStep"
            @click="goToStep(index)"
            :class="'cursor-pointer font-medium'"
          >
            <span class="step-number completed">{{ index + 1 }}</span>
            {{ step.label }}
          </BreadcrumbLink>
          <BreadcrumbPage
            v-else-if="index === currentStep"
            class="flex items-center gap-2"
          >
            <span class="step-number active">{{ index + 1 }}</span>
            {{ step.label }}
          </BreadcrumbPage>
          <span v-else class="flex items-center gap-2 text-muted-foreground">
            <span class="step-number">{{ index + 1 }}</span>
            {{ step.label }}
          </span>
          <BreadcrumbSeparator v-if="index < steps.length - 1" />
        </BreadcrumbItem>
      </BreadcrumbList>
    </Breadcrumb>

    <!-- Step Content -->
    <div class="step-container">
      <PersonalInfoStep v-if="currentStep === 0" v-model="profileData" />
      <WorkExperienceStep v-if="currentStep === 1" v-model="profileData" />
      <EducationSkillsStep v-if="currentStep === 2" v-model="profileData" />
      <ProjectsVolunteeringStep
        v-if="currentStep === 3"
        v-model="profileData"
      />
    </div>

    <!-- Navigation Footer -->
    <div class="action-footer">
      <Button v-if="currentStep > 0" @click="previousStep" variant="outline">
        ← Previous
      </Button>
      <div class="spacer"></div>
      <Button
        v-if="currentStep < steps.length - 1"
        @click="nextStep"
        :disabled="saving"
      >
        {{ saving ? "Saving..." : "Save & Continue →" }}
      </Button>
      <Button v-else @click="finishProfile" :disabled="saving">
        {{ saving ? "Saving..." : "Save & Finish" }}
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Button } from "@/components/ui/button";
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import PersonalInfoStep from "@/components/profile-steps/PersonalInfoStep.vue";
import WorkExperienceStep from "@/components/profile-steps/WorkExperienceStep.vue";
import EducationSkillsStep from "@/components/profile-steps/EducationSkillsStep.vue";
import ProjectsVolunteeringStep from "@/components/profile-steps/ProjectsVolunteeringStep.vue";

const router = useRouter();
const currentStep = ref(0);
const saving = ref(false);

const steps = [
  { label: "Personal Info & Summary", key: "personalInfo" },
  { label: "Work Experience", key: "workExperience" },
  { label: "Education & Skills", key: "educationSkills" },
  { label: "Projects & Volunteering", key: "projectsVolunteering" },
];

const profileData = reactive({
  personalInfo: {
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    location: {
      city: "",
      country: "",
    },
    linkedinUrl: "",
    portfolioUrl: "",
  },
  professionalHeadline: "",
  summary: "",
  workExperience: [],
  education: [],
  skills: [],
  certifications: [],
  projects: [],
  volunteering: [],
  languages: [],
  publications: [],
  jobPreferences: {
    desiredRoles: [],
    desiredRolesText: "",
    employmentTypes: [],
    employmentTypesText: "",
    locations: [],
    locationsText: "",
    openToRelocation: false,
  },
});

onMounted(async () => {
  await loadProfile();
});

async function loadProfile() {
  try {
    const response = await fetch("http://localhost:8000/profile");
    if (response.ok) {
      const data = await response.json();
      if (data.profile) {
        Object.assign(profileData, data.profile);

        // Restore text fields for arrays
        if (profileData.jobPreferences) {
          profileData.jobPreferences.desiredRolesText =
            profileData.jobPreferences.desiredRoles?.join(", ") || "";
          profileData.jobPreferences.employmentTypesText =
            profileData.jobPreferences.employmentTypes?.join(", ") || "";
          profileData.jobPreferences.locationsText =
            profileData.jobPreferences.locations?.join(", ") || "";
        }

        // Restore text fields for work experience
        profileData.workExperience.forEach((exp) => {
          exp.responsibilitiesText = exp.responsibilities?.join("\n• ") || "";
          exp.achievementsText = exp.achievements?.join("\n• ") || "";
          exp.technologiesText = exp.technologies?.join(", ") || "";
        });

        // Restore text fields for projects
        profileData.projects.forEach((project) => {
          project.technologiesText = project.technologies?.join(", ") || "";
        });
      }
    }
  } catch (error) {
    console.error("Failed to load profile:", error);
  }
}

async function saveProfile() {
  saving.value = true;
  try {
    const response = await fetch("http://localhost:8000/profile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ profile: profileData }),
    });

    if (!response.ok) {
      throw new Error("Failed to save profile");
    }

    const result = await response.json();
    console.log("Profile saved:", result);
  } catch (error) {
    console.error("Error saving profile:", error);
    alert("Failed to save profile. Please try again.");
  } finally {
    saving.value = false;
  }
}

async function nextStep() {
  await saveProfile();
  if (currentStep.value < steps.length - 1) {
    currentStep.value++;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

function previousStep() {
  if (currentStep.value > 0) {
    currentStep.value--;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

function goToStep(index) {
  currentStep.value = index;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function finishProfile() {
  await saveProfile();
  router.push("/home");
}
</script>

<style scoped>
.profile-view {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 48px 64px 48px;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}

.page-description {
  font-size: 16px;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

/* Breadcrumb Wrapper */
.breadcrumb-wrapper {
  margin-bottom: 48px;
  padding: 24px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Step Numbers */
.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 600;
  background-color: #e5e7eb;
  color: #9ca3af;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
}

.step-number.active {
  background-color: #3b82f6;
  color: #ffffff;
  border-color: #3b82f6;
}

.step-number.completed {
  background-color: #10b981;
  color: #ffffff;
  border-color: #10b981;
}

/* Step Container */
.step-container {
  min-height: 400px;
  margin-bottom: 32px;
  position: relative;
}

/* Action Footer */
.action-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 0;
  margin: 32px auto 0;
  max-width: 900px;
}

.spacer {
  flex: 1;
}

@media (max-width: 1024px) {
  .profile-view {
    padding: 32px 32px 64px 32px;
  }

  .breadcrumb-wrapper {
    padding: 16px;
  }

  .step-number {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
}

@media (max-width: 768px) {
  .profile-view {
    padding: 24px 20px 64px 20px;
  }

  .breadcrumb-wrapper {
    padding: 12px;
  }

  .step-number {
    width: 24px;
    height: 24px;
    font-size: 11px;
  }
}
</style>
