<template>
  <div class="step-content">
    <div class="step-header-actions">
      <div>
        <h2 class="step-title">Work Experience</h2>
        <p class="step-description">
          Add your professional work history and accomplishments
        </p>
      </div>
      <Button @click="fillDummyData" variant="outline" class="dummy-data-btn">
        <span class="icon">✨</span>
        Fill with Test Data
      </Button>
    </div>

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
          <rect width="20" height="14" x="2" y="7" rx="2" ry="2" />
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
        </svg>
        <h3 class="form-section-title">Work History</h3>
      </div>
      <Dialog
        :open="experienceDialogOpen"
        @update:open="experienceDialogOpen = $event"
      >
        <DialogTrigger>
          <Button variant="outline" class="add-item-btn">
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
            Add Experience
          </Button>
        </DialogTrigger>
        <DialogContent class="max-w-3xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{{
              editingIndex !== null
                ? "Edit Work Experience"
                : "Add Work Experience"
            }}</DialogTitle>
            <DialogDescription>
              {{
                editingIndex !== null
                  ? "Update your professional work experience details."
                  : "Add your professional work experience details."
              }}
            </DialogDescription>
          </DialogHeader>
          <form @submit="onExperienceSubmit" class="dialog-form">
            <div class="form-row">
              <div class="form-group">
                <label>Job Title <span class="required">*</span></label>
                <input
                  v-model="experienceForm.jobTitle"
                  type="text"
                  placeholder="Senior Software Engineer"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                />
              </div>

              <div class="form-group">
                <label>Company Name <span class="required">*</span></label>
                <input
                  v-model="experienceForm.companyName"
                  type="text"
                  placeholder="Tech Company Inc."
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Employment Type</label>
                <select
                  v-model="experienceForm.employmentType"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  <option value="Full-time">Full-time</option>
                  <option value="Part-time">Part-time</option>
                  <option value="Contract">Contract</option>
                  <option value="Internship">Internship</option>
                  <option value="Freelance">Freelance</option>
                </select>
              </div>

              <div class="form-group">
                <label>Location</label>
                <input
                  v-model="experienceForm.location"
                  type="text"
                  placeholder="San Francisco, CA"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Start Date <span class="required">*</span></label>
                <input
                  v-model="experienceForm.startDate"
                  type="month"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                />
              </div>

              <div class="form-group">
                <label>End Date</label>
                <input
                  v-model="experienceForm.endDate"
                  type="month"
                  :disabled="experienceForm.currentlyWorking"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                />
              </div>
            </div>

            <div class="form-group">
              <label class="checkbox-label flex items-center gap-2">
                <input
                  v-model="experienceForm.currentlyWorking"
                  type="checkbox"
                  @change="handleCurrentlyWorkingChange"
                />
                <span>I currently work here</span>
              </label>
            </div>

            <div class="form-group">
              <label>Responsibilities</label>
              <textarea
                v-model="experienceForm.responsibilitiesText"
                rows="4"
                placeholder="• Led development of customer-facing web application&#10;• Managed team of 5 engineers&#10;• Implemented CI/CD pipeline"
                class="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              ></textarea>
              <small class="help-text"
                >Start each item with a bullet point (•) or dash (-)</small
              >
            </div>

            <div class="form-group">
              <label>Achievements</label>
              <textarea
                v-model="experienceForm.achievementsText"
                rows="4"
                placeholder="• Improved application performance by 40%&#10;• Reduced deployment time from 2 hours to 15 minutes"
                class="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              ></textarea>
              <small class="help-text"
                >Start each item with a bullet point (•) or dash (-)</small
              >
            </div>

            <div class="form-group">
              <label>Technologies Used</label>
              <input
                v-model="experienceForm.technologiesText"
                type="text"
                placeholder="React, Node.js, PostgreSQL, AWS, Docker"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
              <small class="help-text">Separate with commas</small>
            </div>

            <DialogFooter>
              <Button
                @click="experienceDialogOpen = false"
                variant="outline"
                type="button"
                :disabled="isSaving"
              >
                Cancel
              </Button>
              <Button type="submit" :disabled="isSaving">
                {{
                  isSaving
                    ? "Saving..."
                    : editingIndex !== null
                    ? "Update Experience"
                    : "Save Experience"
                }}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>

    <!-- Experience List -->
    <div v-if="formData.workExperience.length > 0" class="experiences-list">
      <Card
        v-for="(exp, index) in formData.workExperience"
        :key="index"
        class="experience-card"
      >
        <CardContent class="pt-6">
          <div class="card-header">
            <div>
              <h3 class="experience-title">{{ exp.jobTitle }}</h3>
              <p class="experience-company">{{ exp.companyName }}</p>
              <p class="experience-meta">
                {{ exp.location }} • {{ exp.employmentType }} •
                {{ formatDate(exp.startDate) }} -
                {{ exp.currentlyWorking ? "Present" : formatDate(exp.endDate) }}
              </p>
            </div>
            <div class="card-actions">
              <Button
                @click="editExperience(index)"
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
                  <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" />
                  <path d="m15 5 4 4" />
                </svg>
              </Button>
              <Button
                @click="removeExperience(index)"
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

          <!-- Responsibilities -->
          <div
            v-if="exp.responsibilities && exp.responsibilities.length > 0"
            class="experience-section"
          >
            <h4 class="section-label">Responsibilities</h4>
            <ul class="experience-list">
              <li v-for="(item, idx) in exp.responsibilities" :key="idx">
                {{ item }}
              </li>
            </ul>
          </div>

          <!-- Achievements -->
          <div
            v-if="exp.achievements && exp.achievements.length > 0"
            class="experience-section"
          >
            <h4 class="section-label">Achievements</h4>
            <ul class="experience-list">
              <li v-for="(item, idx) in exp.achievements" :key="idx">
                {{ item }}
              </li>
            </ul>
          </div>

          <!-- Technologies -->
          <div
            v-if="exp.technologies && exp.technologies.length > 0"
            class="experience-section"
          >
            <h4 class="section-label">Technologies</h4>
            <div class="tech-tags">
              <span
                v-for="(tech, idx) in exp.technologies"
                :key="idx"
                class="tech-tag"
              >
                {{ tech }}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <div v-else class="empty-state">
      <p>
        No work experience added yet. Click "Add Experience" to get started.
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, watch } from "vue";
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

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue"]);

const auth = useAuth();
const formData = props.modelValue;
const experienceDialogOpen = ref(false);
const isSaving = ref(false);
const editingIndex = ref(null); // null means adding new, number means editing

const experienceForm = ref({
  jobTitle: "",
  companyName: "",
  employmentType: "Full-time",
  location: "",
  startDate: "",
  endDate: "",
  currentlyWorking: false,
  responsibilitiesText: "",
  achievementsText: "",
  technologiesText: "",
});

// Reset form when dialog closes
watch(experienceDialogOpen, (isOpen) => {
  if (!isOpen) {
    resetExperienceForm();
    editingIndex.value = null;
  }
});

function resetExperienceForm() {
  experienceForm.value = {
    jobTitle: "",
    companyName: "",
    employmentType: "Full-time",
    location: "",
    startDate: "",
    endDate: "",
    currentlyWorking: false,
    responsibilitiesText: "",
    achievementsText: "",
    technologiesText: "",
  };
}

function handleCurrentlyWorkingChange() {
  if (experienceForm.value.currentlyWorking) {
    experienceForm.value.endDate = "";
  }
}

async function onExperienceSubmit(event) {
  event.preventDefault();
  isSaving.value = true;

  try {
    // Parse text fields into arrays
    const responsibilities = experienceForm.value.responsibilitiesText
      ? experienceForm.value.responsibilitiesText
          .split("\n")
          .map((line) => line.trim().replace(/^[•\-]\s*/, ""))
          .filter((line) => line.length > 0)
      : [];

    const achievements = experienceForm.value.achievementsText
      ? experienceForm.value.achievementsText
          .split("\n")
          .map((line) => line.trim().replace(/^[•\-]\s*/, ""))
          .filter((line) => line.length > 0)
      : [];

    const technologies = experienceForm.value.technologiesText
      ? experienceForm.value.technologiesText
          .split(",")
          .map((tech) => tech.trim())
          .filter((tech) => tech.length > 0)
      : [];

    const experienceData = {
      jobTitle: experienceForm.value.jobTitle,
      companyName: experienceForm.value.companyName,
      employmentType: experienceForm.value.employmentType,
      location: experienceForm.value.location,
      startDate: experienceForm.value.startDate,
      endDate: experienceForm.value.endDate,
      currentlyWorking: experienceForm.value.currentlyWorking,
      responsibilities,
      achievements,
      technologies,
    };

    // Update local state
    if (editingIndex.value !== null) {
      // Update existing experience
      formData.workExperience[editingIndex.value] = experienceData;
      console.log(
        "[WorkExperienceStep] Updating experience at index:",
        editingIndex.value
      );
    } else {
      // Add new experience
      formData.workExperience.push(experienceData);
      console.log("[WorkExperienceStep] Adding new experience");
    }

    // Save to database immediately
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        workExperience: formData.workExperience,
      });
      console.log("[WorkExperienceStep] Work experience saved to database");
    }

    // Reset form and close dialog
    resetExperienceForm();
    editingIndex.value = null;
    experienceDialogOpen.value = false;
  } catch (error) {
    console.error("[WorkExperienceStep] Error saving experience:", error);
    alert("Failed to save experience. Please try again.");
  } finally {
    isSaving.value = false;
  }
}

async function removeExperience(index) {
  const removedExperience = formData.workExperience[index];

  // Remove from local state
  formData.workExperience.splice(index, 1);

  try {
    // Save to database immediately
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        workExperience: formData.workExperience,
      });
      console.log(
        "[WorkExperienceStep] Work experience removed and saved to database"
      );
    }
  } catch (error) {
    console.error("[WorkExperienceStep] Failed to remove experience:", error);
    // Restore the experience if save failed
    formData.workExperience.splice(index, 0, removedExperience);
    alert("Failed to remove experience. Please try again.");
  }
}

function editExperience(index) {
  const exp = formData.workExperience[index];

  // Populate form with existing data
  experienceForm.value = {
    jobTitle: exp.jobTitle || "",
    companyName: exp.companyName || "",
    employmentType: exp.employmentType || "Full-time",
    location: exp.location || "",
    startDate: exp.startDate || "",
    endDate: exp.endDate || "",
    currentlyWorking: exp.currentlyWorking || false,
    responsibilitiesText: exp.responsibilities?.join("\n• ") || "",
    achievementsText: exp.achievements?.join("\n• ") || "",
    technologiesText: exp.technologies?.join(", ") || "",
  };

  editingIndex.value = index;
  experienceDialogOpen.value = true;
}

function formatDate(dateString) {
  if (!dateString) return "";
  const [year, month] = dateString.split("-");
  const date = new Date(year, month - 1);
  return date.toLocaleDateString("en-US", { month: "short", year: "numeric" });
}

async function fillDummyData() {
  try {
    console.log("[WorkExperienceStep] Filling with test data");

    const dummyWorkExperience = [
      {
        jobTitle: "Senior Full-Stack Developer",
        companyName: "TechCorp Solutions",
        employmentType: "Full-time",
        location: "San Francisco, CA",
        startDate: "2020-03",
        endDate: "",
        currentlyWorking: true,
        responsibilitiesText:
          "• Led development of microservices architecture serving 2M+ users\n• Mentored team of 5 junior developers and conducted code reviews\n• Architected and implemented CI/CD pipeline reducing deployment time by 60%\n• Collaborated with product team to define technical requirements and roadmap",
        responsibilities: [
          "Led development of microservices architecture serving 2M+ users",
          "Mentored team of 5 junior developers and conducted code reviews",
          "Architected and implemented CI/CD pipeline reducing deployment time by 60%",
          "Collaborated with product team to define technical requirements and roadmap",
        ],
        achievementsText:
          "• Improved application performance by 45% through optimization and caching strategies\n• Reduced bug count by 70% by implementing comprehensive testing suite\n• Received 'Outstanding Performance' award for Q3 2023",
        achievements: [
          "Improved application performance by 45% through optimization and caching strategies",
          "Reduced bug count by 70% by implementing comprehensive testing suite",
          "Received 'Outstanding Performance' award for Q3 2023",
        ],
        technologiesText:
          "React, Node.js, TypeScript, PostgreSQL, AWS, Docker, Kubernetes, GraphQL, Redis",
        technologies: [
          "React",
          "Node.js",
          "TypeScript",
          "PostgreSQL",
          "AWS",
          "Docker",
          "Kubernetes",
          "GraphQL",
          "Redis",
        ],
      },
      {
        jobTitle: "Full-Stack Developer",
        companyName: "StartupHub Inc",
        employmentType: "Full-time",
        location: "Remote",
        startDate: "2018-01",
        endDate: "2020-02",
        currentlyWorking: false,
        responsibilitiesText:
          "• Developed and maintained web applications using React and Node.js\n• Built RESTful APIs and integrated third-party services\n• Implemented responsive UI components following design specifications\n• Participated in agile ceremonies and sprint planning",
        responsibilities: [
          "Developed and maintained web applications using React and Node.js",
          "Built RESTful APIs and integrated third-party services",
          "Implemented responsive UI components following design specifications",
          "Participated in agile ceremonies and sprint planning",
        ],
        achievementsText:
          "• Successfully launched 3 major features ahead of schedule\n• Reduced API response time by 30% through optimization\n• Contributed to 95% code coverage through unit and integration tests",
        achievements: [
          "Successfully launched 3 major features ahead of schedule",
          "Reduced API response time by 30% through optimization",
          "Contributed to 95% code coverage through unit and integration tests",
        ],
        technologiesText: "React, Node.js, Express, MongoDB, Jest, Git, Jira",
        technologies: [
          "React",
          "Node.js",
          "Express",
          "MongoDB",
          "Jest",
          "Git",
          "Jira",
        ],
      },
      {
        jobTitle: "Junior Software Developer",
        companyName: "Digital Innovations Ltd",
        employmentType: "Full-time",
        location: "New York, NY",
        startDate: "2016-06",
        endDate: "2017-12",
        currentlyWorking: false,
        responsibilitiesText:
          "• Assisted in developing front-end features using HTML, CSS, and JavaScript\n• Fixed bugs and performed code maintenance on existing applications\n• Collaborated with senior developers on feature implementation\n• Participated in daily standups and code reviews",
        responsibilities: [
          "Assisted in developing front-end features using HTML, CSS, and JavaScript",
          "Fixed bugs and performed code maintenance on existing applications",
          "Collaborated with senior developers on feature implementation",
          "Participated in daily standups and code reviews",
        ],
        achievementsText:
          "• Resolved 150+ bugs during tenure\n• Implemented automated testing reducing manual QA time by 40%\n• Recognized as 'Most Improved Developer' in 2017",
        achievements: [
          "Resolved 150+ bugs during tenure",
          "Implemented automated testing reducing manual QA time by 40%",
          "Recognized as 'Most Improved Developer' in 2017",
        ],
        technologiesText: "JavaScript, HTML, CSS, jQuery, Bootstrap, MySQL",
        technologies: [
          "JavaScript",
          "HTML",
          "CSS",
          "jQuery",
          "Bootstrap",
          "MySQL",
        ],
      },
    ];

    // Save directly to database
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        workExperience: dummyWorkExperience,
      });
      console.log("[WorkExperienceStep] Test data saved to database");

      // Update local state to reflect saved data
      formData.workExperience = dummyWorkExperience;

      alert("Test data filled and saved successfully!");
    }
  } catch (error) {
    console.error("[WorkExperienceStep] Error filling test data:", error);
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
  margin-bottom: 24px;
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
  margin: 0 0 24px 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.form-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-actions {
  display: flex;
  gap: 4px;
}

.form-section-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.remove-btn {
  color: #ef4444;
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

/* Experience List */
.experiences-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 20px;
}

.experience-card {
  border: 1px solid #e5e7eb;
  transition: border-color 0.2s ease;
}

.experience-card:hover {
  border-color: #d1d5db;
}

.experience-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 4px 0;
}

.experience-company {
  font-size: 15px;
  font-weight: 500;
  color: #3b82f6;
  margin: 0 0 4px 0;
}

.experience-meta {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

.experience-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.section-label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px 0;
}

.experience-list {
  margin: 0;
  padding-left: 20px;
  list-style-type: disc;
}

.experience-list li {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 4px;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-tag {
  display: inline-block;
  padding: 4px 12px;
  background-color: #eff6ff;
  color: #1e40af;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

/* Dialog Form Styles */
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

.help-text {
  display: block;
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
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

.list-input {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.help-text {
  font-size: 12px;
  color: #64748b;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
  font-size: 14px;
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

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
