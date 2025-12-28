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
      <Button @click="addExperience" variant="outline">
        + Add Experience
      </Button>
    </div>

    <Card
      v-for="(exp, index) in formData.workExperience"
      :key="index"
      class="form-card"
    >
      <CardContent class="pt-6">
        <div class="card-header">
          <h3 class="form-section-title">Experience {{ index + 1 }}</h3>
          <Button
            @click="removeExperience(index)"
            size="sm"
            variant="ghost"
            class="remove-btn"
          >
            ✕ Remove
          </Button>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Job Title <span class="required">*</span></label>
            <input
              v-model="exp.jobTitle"
              type="text"
              required
              placeholder="Senior Software Engineer"
            />
          </div>

          <div class="form-group">
            <label>Company Name <span class="required">*</span></label>
            <input
              v-model="exp.companyName"
              type="text"
              required
              placeholder="Tech Company Inc."
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Employment Type</label>
            <select v-model="exp.employmentType">
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
              v-model="exp.location"
              type="text"
              placeholder="San Francisco, CA"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Start Date <span class="required">*</span></label>
            <input v-model="exp.startDate" type="month" required />
          </div>

          <div class="form-group">
            <label>End Date</label>
            <input
              v-model="exp.endDate"
              type="month"
              :disabled="exp.currentlyWorking"
              :placeholder="exp.currentlyWorking ? 'Present' : ''"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              v-model="exp.currentlyWorking"
              type="checkbox"
              @change="() => exp.currentlyWorking && (exp.endDate = '')"
            />
            <span>I currently work here</span>
          </label>
        </div>

        <div class="form-group">
          <label>Responsibilities</label>
          <div class="list-input">
            <textarea
              v-model="exp.responsibilitiesText"
              rows="4"
              placeholder="• Led development of customer-facing web application&#10;• Managed team of 5 engineers&#10;• Implemented CI/CD pipeline"
              @input="updateResponsibilities(exp)"
            ></textarea>
            <small class="help-text"
              >Start each item with a bullet point (•) or dash (-)</small
            >
          </div>
        </div>

        <div class="form-group">
          <label>Achievements</label>
          <div class="list-input">
            <textarea
              v-model="exp.achievementsText"
              rows="4"
              placeholder="• Improved application performance by 40%&#10;• Reduced deployment time from 2 hours to 15 minutes&#10;• Launched product feature used by 100k+ users"
              @input="updateAchievements(exp)"
            ></textarea>
            <small class="help-text"
              >Start each item with a bullet point (•) or dash (-)</small
            >
          </div>
        </div>

        <div class="form-group">
          <label>Technologies Used</label>
          <input
            v-model="exp.technologiesText"
            type="text"
            placeholder="React, Node.js, PostgreSQL, AWS, Docker"
            @input="updateTechnologies(exp)"
          />
          <small class="help-text">Separate with commas</small>
        </div>
      </CardContent>
    </Card>

    <div v-if="formData.workExperience.length === 0" class="empty-state">
      <p>
        No work experience added yet. Click "Add Experience" to get started.
      </p>
    </div>
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

function addExperience() {
  formData.workExperience.push({
    jobTitle: "",
    companyName: "",
    employmentType: "Full-time",
    location: "",
    startDate: "",
    endDate: "",
    currentlyWorking: false,
    responsibilities: [],
    responsibilitiesText: "",
    achievements: [],
    achievementsText: "",
    technologies: [],
    technologiesText: "",
  });
}

function removeExperience(index) {
  formData.workExperience.splice(index, 1);
}

function updateResponsibilities(exp) {
  exp.responsibilities = exp.responsibilitiesText
    .split("\n")
    .map((line) => line.trim().replace(/^[•\-]\s*/, ""))
    .filter((line) => line.length > 0);
}

function updateAchievements(exp) {
  exp.achievements = exp.achievementsText
    .split("\n")
    .map((line) => line.trim().replace(/^[•\-]\s*/, ""))
    .filter((line) => line.length > 0);
}

function updateTechnologies(exp) {
  exp.technologies = exp.technologiesText
    .split(",")
    .map((tech) => tech.trim())
    .filter((tech) => tech.length > 0);
}

function fillDummyData() {
  formData.workExperience = [
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
  justify-content: flex-start;
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

.form-section-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.remove-btn {
  color: #ef4444;
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
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
