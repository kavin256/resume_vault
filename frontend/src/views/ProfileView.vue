<template>
  <div class="profile-view">
    <!-- Import Options Dialog -->
    <Dialog :open="showImportDialog" @update:open="showImportDialog = $event">
      <DialogContent class="import-dialog-content">
        <ProfileImportOptions
          @resume-upload="handleResumeUpload"
          @linkedin-import="handleLinkedInImport"
          @skip="closeImportDialog"
        />
      </DialogContent>
    </Dialog>

    <!-- Regular Profile Form -->
    <div class="profile-content">
      <div class="page-header">
        <h1>Master Profile</h1>
        <p class="page-description">
          Build your comprehensive professional profile step by step
        </p>
      </div>

      <!-- Import Data Card -->
      <Card class="import-card">
        <CardContent class="import-card-content">
          <div class="import-info">
            <div class="import-icon">
              <svg
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
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" x2="12" y1="15" y2="3" />
              </svg>
            </div>
            <div class="import-text">
              <h3 class="import-title">Quick Import</h3>
              <p class="import-description">
                Save time by importing your professional information from an
                existing resume or your LinkedIn profile. Your imported data
                will be merged with any existing information.
              </p>
            </div>
          </div>
          <Button
            @click="openImportDialog"
            class="import-trigger-btn"
            size="lg"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="btn-icon"
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" x2="12" y1="15" y2="3" />
            </svg>
            Import Data
          </Button>
        </CardContent>
      </Card>

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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@clerk/vue";
import { useUserSync } from "@/composables/useUserSync";
import { getMasterProfile, updateMasterProfile } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import ProfileImportOptions from "@/components/ProfileImportOptions.vue";
import PersonalInfoStep from "@/components/profile-steps/PersonalInfoStep.vue";
import WorkExperienceStep from "@/components/profile-steps/WorkExperienceStep.vue";
import EducationSkillsStep from "@/components/profile-steps/EducationSkillsStep.vue";
import ProjectsVolunteeringStep from "@/components/profile-steps/ProjectsVolunteeringStep.vue";

const router = useRouter();
const auth = useAuth();
const { masterProfile, isLoadingProfile } = useUserSync();
const currentStep = ref(0);
const saving = ref(false);

// Import dialog state
const showImportDialog = ref(false);

// Track original profile data for change detection
const originalProfileData = ref(null);

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
    // If profile is already loaded from useUserSync, use it
    if (masterProfile.value) {
      console.log("[ProfileView] Using profile from useUserSync");
      Object.assign(profileData, masterProfile.value);
      restoreTextFields();
      // Store original data for change detection
      originalProfileData.value = JSON.parse(
        JSON.stringify(masterProfile.value)
      );
      return;
    }

    // Otherwise, fetch it directly
    console.log("[ProfileView] Fetching profile directly");
    const token = await auth.getToken.value();
    if (!token) {
      console.error("[ProfileView] No auth token available");
      return;
    }

    const response = await getMasterProfile(token);
    if (response && response.profile) {
      Object.assign(profileData, response.profile);
      restoreTextFields();
      // Store original data for change detection
      originalProfileData.value = JSON.parse(JSON.stringify(response.profile));
      console.log(`[ProfileView] Profile ${response.status}`);
    }
  } catch (error) {
    console.error("[ProfileView] Failed to load profile:", error);
  }
}

function restoreTextFields() {
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
  if (profileData.workExperience) {
    profileData.workExperience.forEach((exp) => {
      exp.responsibilitiesText = exp.responsibilities?.join("\n• ") || "";
      exp.achievementsText = exp.achievements?.join("\n• ") || "";
      exp.technologiesText = exp.technologies?.join(", ") || "";
    });
  }

  // Restore text fields for projects
  if (profileData.projects) {
    profileData.projects.forEach((project) => {
      project.technologiesText = project.technologies?.join(", ") || "";
    });
  }
}

/**
 * Check if specific fields have changed
 * @param {Array<string>} fields - Array of dot-notation field paths to check
 * @returns {boolean} - True if any field has changed
 */
function hasChanges(fields) {
  if (!originalProfileData.value) return true; // If no original data, assume changes

  for (const field of fields) {
    const currentValue = getNestedValue(profileData, field);
    const originalValue = getNestedValue(originalProfileData.value, field);

    // Deep comparison for objects and arrays
    if (JSON.stringify(currentValue) !== JSON.stringify(originalValue)) {
      return true;
    }
  }

  return false;
}

/**
 * Get nested value from object using dot notation
 * @param {Object} obj - Object to get value from
 * @param {string} path - Dot-notation path (e.g., 'personalInfo.firstName')
 * @returns {any} - Value at path
 */
function getNestedValue(obj, path) {
  return path.split(".").reduce((current, key) => current?.[key], obj);
}

/**
 * Save profile with change detection
 * @param {Array<string>} fieldsToCheck - Optional array of field paths to check for changes
 * @returns {Promise<boolean>} - True if saved, false if no changes
 */
async function saveProfile(fieldsToCheck = null) {
  // If specific fields provided, check only those fields
  if (fieldsToCheck && fieldsToCheck.length > 0) {
    if (!hasChanges(fieldsToCheck)) {
      console.log("[ProfileView] No changes detected, skipping save");
      return false;
    }
  }

  saving.value = true;
  try {
    const token = await auth.getToken.value();
    if (!token) {
      throw new Error("No authentication token available");
    }

    const response = await updateMasterProfile(token, profileData);
    console.log("[ProfileView] Profile saved:", response.status);

    // Update original data after successful save
    originalProfileData.value = JSON.parse(JSON.stringify(profileData));
    return true;
  } catch (error) {
    console.error("[ProfileView] Error saving profile:", error);
    alert("Failed to save profile. Please try again.");
    return false;
  } finally {
    saving.value = false;
  }
}

async function nextStep() {
  // For Personal Info step (step 0), check only Personal Info and Professional Profile fields
  if (currentStep.value === 0) {
    const personalInfoFields = [
      "personalInfo.firstName",
      "personalInfo.lastName",
      "personalInfo.email",
      "personalInfo.phone",
      "personalInfo.location.city",
      "personalInfo.location.country",
      "personalInfo.linkedinUrl",
      "personalInfo.portfolioUrl",
      "professionalHeadline",
      "summary",
      "languages",
    ];
    await saveProfile(personalInfoFields);
  } else {
    // For other steps, save everything
    await saveProfile();
  }

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
  saving.value = true;

  try {
    // Check if job preferences have any data
    const hasJobPreferences =
      profileData.jobPreferences.desiredRolesText?.trim() ||
      profileData.jobPreferences.employmentTypesText?.trim() ||
      profileData.jobPreferences.locationsText?.trim() ||
      profileData.jobPreferences.openToRelocation;

    if (hasJobPreferences) {
      console.log("[ProfileView] Saving job preferences");

      // Parse comma-separated text fields to arrays
      const desiredRoles =
        profileData.jobPreferences.desiredRolesText
          ?.split(",")
          .map((role) => role.trim())
          .filter((role) => role.length > 0) || [];

      const employmentTypes =
        profileData.jobPreferences.employmentTypesText
          ?.split(",")
          .map((type) => type.trim())
          .filter((type) => type.length > 0) || [];

      const locations =
        profileData.jobPreferences.locationsText
          ?.split(",")
          .map((loc) => loc.trim())
          .filter((loc) => loc.length > 0) || [];

      const token = await auth.getToken.value();
      if (token) {
        await updateMasterProfile(token, {
          jobPreferences: {
            desiredRoles,
            employmentTypes,
            locations,
            openToRelocation:
              profileData.jobPreferences.openToRelocation || false,
          },
        });
        console.log("[ProfileView] Job preferences saved successfully");
      }
    } else {
      console.log("[ProfileView] No job preferences to save");
    }

    // Navigate to Home vault screen
    router.push("/home");
  } catch (error) {
    console.error("[ProfileView] Error saving job preferences:", error);
    alert("Failed to save job preferences. Please try again.");
  } finally {
    saving.value = false;
  }
}

// Import Dialog Controls
function openImportDialog() {
  showImportDialog.value = true;
}

function closeImportDialog() {
  showImportDialog.value = false;
}

// Helper function to merge imported data with existing data
function mergeProfileData(importedData) {
  if (!importedData) return;

  // Update personal info (replace existing)
  if (importedData.personalInfo) {
    Object.assign(profileData.personalInfo, importedData.personalInfo);
  }

  // Update professional headline and summary (replace existing)
  if (importedData.professionalHeadline) {
    profileData.professionalHeadline = importedData.professionalHeadline;
  }
  if (importedData.professionalSummary) {
    profileData.summary = importedData.professionalSummary;
  }
  if (importedData.summary) {
    profileData.summary = importedData.summary;
  }

  // Merge work experience (add new, avoid duplicates by comparing job title and company)
  if (
    importedData.workExperience &&
    Array.isArray(importedData.workExperience)
  ) {
    importedData.workExperience.forEach((newExp) => {
      const exists = profileData.workExperience.some(
        (exp) =>
          exp.jobTitle === newExp.jobTitle &&
          exp.companyName === newExp.companyName &&
          exp.startDate === newExp.startDate
      );
      if (!exists) {
        profileData.workExperience.push(newExp);
      }
    });
  }

  // Merge education (add new, avoid duplicates by comparing institution and degree)
  if (importedData.education && Array.isArray(importedData.education)) {
    importedData.education.forEach((newEdu) => {
      const exists = profileData.education.some(
        (edu) =>
          edu.institution === newEdu.institution &&
          edu.degree === newEdu.degree &&
          edu.startYear === newEdu.startYear
      );
      if (!exists) {
        profileData.education.push(newEdu);
      }
    });
  }

  // Merge skills (add new, avoid duplicates by name)
  if (importedData.skills && Array.isArray(importedData.skills)) {
    importedData.skills.forEach((newSkill) => {
      const exists = profileData.skills.some(
        (skill) => skill.name.toLowerCase() === newSkill.name.toLowerCase()
      );
      if (!exists) {
        profileData.skills.push(newSkill);
      }
    });
  }

  // Merge certifications (add new, avoid duplicates by name)
  if (
    importedData.certifications &&
    Array.isArray(importedData.certifications)
  ) {
    importedData.certifications.forEach((newCert) => {
      const exists = profileData.certifications.some(
        (cert) =>
          cert.name === newCert.name &&
          cert.issuingOrganization === newCert.issuingOrganization
      );
      if (!exists) {
        profileData.certifications.push(newCert);
      }
    });
  }

  // Merge projects (add new, avoid duplicates by title)
  if (importedData.projects && Array.isArray(importedData.projects)) {
    importedData.projects.forEach((newProj) => {
      const exists = profileData.projects.some(
        (proj) => proj.title === newProj.title
      );
      if (!exists) {
        profileData.projects.push(newProj);
      }
    });
  }

  // Merge volunteering (add new, avoid duplicates by organization and role)
  if (importedData.volunteering && Array.isArray(importedData.volunteering)) {
    importedData.volunteering.forEach((newVol) => {
      const exists = profileData.volunteering.some(
        (vol) =>
          vol.organization === newVol.organization && vol.role === newVol.role
      );
      if (!exists) {
        profileData.volunteering.push(newVol);
      }
    });
  }

  // Merge languages (add new, avoid duplicates by language name)
  if (importedData.languages && Array.isArray(importedData.languages)) {
    importedData.languages.forEach((newLang) => {
      const exists = profileData.languages.some(
        (lang) => lang.language.toLowerCase() === newLang.language.toLowerCase()
      );
      if (!exists) {
        profileData.languages.push(newLang);
      }
    });
  }

  // Merge publications (add new, avoid duplicates by title)
  if (importedData.publications && Array.isArray(importedData.publications)) {
    importedData.publications.forEach((newPub) => {
      const exists = profileData.publications.some(
        (pub) => pub.title === newPub.title
      );
      if (!exists) {
        profileData.publications.push(newPub);
      }
    });
  }

  // Update job preferences (replace existing)
  if (importedData.jobPreferences) {
    Object.assign(profileData.jobPreferences, importedData.jobPreferences);
  }
}

// Import Options Handlers
async function handleResumeUpload(file) {
  console.log("[ProfileView] Resume upload initiated:", file.name);

  try {
    saving.value = true;

    // Placeholder for future implementation
    alert(
      "Resume upload feature will be implemented soon. The file has been received: " +
        file.name
    );

    closeImportDialog();
  } catch (error) {
    console.error("[ProfileView] Resume upload failed:", error);
    alert("Failed to upload resume. Please try again.");
  } finally {
    saving.value = false;
  }
}

async function handleLinkedInImport() {
  console.log("[ProfileView] LinkedIn import initiated");

  try {
    saving.value = true;

    // TODO: Implement LinkedIn OAuth and import API call
    // const token = await auth.getToken.value();
    // const response = await importFromLinkedIn(token);
    //
    // Merge the LinkedIn data with existing profile
    // mergeProfileData(response.linkedInData);
    //
    // Save merged data to database
    // await updateMasterProfile(token, profileData);

    // For now, show a message
    alert(
      "LinkedIn import feature will be implemented soon.\n\nWhen implemented, it will merge your LinkedIn data with your existing profile."
    );

    closeImportDialog();
  } catch (error) {
    console.error("[ProfileView] LinkedIn import failed:", error);
    alert("Failed to import from LinkedIn. Please try again.");
  } finally {
    saving.value = false;
  }
}
</script>

<style scoped>
.profile-view {
  width: 100%;
  margin: 0 auto;
  min-height: 100vh;
}

/* Dialog Content Styles */
.import-dialog-content {
  max-width: 550px;
  max-height: 85vh;
  overflow-y: auto;
  padding: 0;
  border: 0;
}

@media (max-width: 640px) {
  .import-dialog-content {
    max-width: 95vw;
    max-height: 90vh;
  }
}

.profile-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 24px 64px 24px;
}

@media (min-width: 768px) {
  .profile-content {
    padding: 40px 48px 64px 48px;
  }
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}

@media (max-width: 640px) {
  .page-header h1 {
    font-size: 26px;
  }
}

.page-description {
  font-size: 16px;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 640px) {
  .page-description {
    font-size: 14px;
  }
}

/* Import Card */
.import-card {
  margin-bottom: 32px;
  border: 2px solid #e2e8f0;
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.import-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
  transform: translateY(-2px);
}

.import-card-content {
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

@media (max-width: 768px) {
  .import-card-content {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }
}

.import-info {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  flex: 1;
}

@media (max-width: 768px) {
  .import-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}

.import-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.import-text {
  flex: 1;
}

.import-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 8px 0;
}

@media (max-width: 640px) {
  .import-title {
    font-size: 16px;
  }
}

.import-description {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

@media (max-width: 640px) {
  .import-description {
    font-size: 13px;
  }
}

.import-trigger-btn {
  flex-shrink: 0;
  min-width: 160px;
  height: 48px;
  padding: 0 28px;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  transition: all 0.2s ease;
}

.import-trigger-btn:hover {
  background: linear-gradient(135deg, #5568d3 0%, #63408b 100%);
  transform: scale(1.02);
}

@media (max-width: 768px) {
  .import-trigger-btn {
    width: 100%;
  }
}

.btn-icon {
  flex-shrink: 0;
}

/* Breadcrumb Wrapper */
.breadcrumb-wrapper {
  margin-bottom: 32px;
  padding: 20px 28px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.breadcrumb-wrapper:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

@media (max-width: 768px) {
  .breadcrumb-wrapper {
    padding: 16px 20px;
    margin-bottom: 24px;
  }
}

/* Step Numbers */
.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 700;
  background: #ffffff;
  color: #94a3b8;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.step-number.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transform: scale(1.05);
}

.step-number.completed {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #ffffff;
  border-color: #10b981;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.25);
}

/* Step Container */
.step-container {
  min-height: 400px;
  margin-bottom: 40px;
  position: relative;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Action Footer */
.action-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 24px 0;
  margin: 0 auto;
  max-width: 900px;
}

@media (max-width: 768px) {
  .action-footer {
    padding: 24px 0;
    flex-wrap: wrap;
  }
}

.spacer {
  flex: 1;
}

.action-footer button:not([variant="outline"]) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
}

.action-footer button:not([variant="outline"]):hover {
  background: linear-gradient(135deg, #5568d3 0%, #653a8a 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
}

.action-footer button[variant="outline"] {
  background: white;
  color: #667eea;
  border: 2px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-footer button[variant="outline"]:hover {
  background-image: linear-gradient(135deg, #f8f9ff 0%, #faf8ff 100%), linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translateY(-2px);
  color: #5568d3;
}

@media (max-width: 1024px) {
  .profile-view {
    padding: 32px 32px 64px 32px;
  }

  .step-number {
    width: 32px;
    height: 32px;
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .profile-view {
    padding: 24px 20px 64px 20px;
  }

  .step-number {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
}
</style>
