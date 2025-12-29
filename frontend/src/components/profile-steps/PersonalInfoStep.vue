<template>
  <div class="step-content">
    <div class="step-header-actions">
      <div>
        <h2 class="step-title">Personal Information & Summary</h2>
        <p class="step-description">
          Tell us about yourself and your professional background
        </p>
      </div>
      <Button @click="fillDummyData" variant="outline" class="dummy-data-btn">
        <span class="icon">✨</span>
        Fill with Test Data
      </Button>
    </div>

    <!-- Personal Information -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <h3 class="form-section-title">Personal Details</h3>

        <div class="form-row">
          <div class="form-group">
            <label>First Name <span class="required">*</span></label>
            <input
              v-model="formData.personalInfo.firstName"
              type="text"
              required
            />
          </div>

          <div class="form-group">
            <label>Last Name <span class="required">*</span></label>
            <input
              v-model="formData.personalInfo.lastName"
              type="text"
              required
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Email <span class="required">*</span></label>
            <input
              v-model="formData.personalInfo.email"
              type="email"
              required
            />
          </div>

          <div class="form-group">
            <label>Phone <span class="required">*</span></label>
            <input
              v-model="formData.personalInfo.phone"
              type="tel"
              required
              placeholder="+1 (555) 123-4567"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>City</label>
            <input
              v-model="formData.personalInfo.location.city"
              type="text"
              placeholder="San Francisco"
            />
          </div>

          <div class="form-group">
            <label>Country</label>
            <input
              v-model="formData.personalInfo.location.country"
              type="text"
              placeholder="United States"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>LinkedIn URL</label>
            <input
              v-model="formData.personalInfo.linkedinUrl"
              type="url"
              placeholder="https://linkedin.com/in/yourprofile"
            />
          </div>

          <div class="form-group">
            <label>Portfolio URL</label>
            <input
              v-model="formData.personalInfo.portfolioUrl"
              type="url"
              placeholder="https://yourportfolio.com"
            />
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Professional Summary -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <h3 class="form-section-title">Professional Profile</h3>

        <div class="form-group">
          <label>Professional Headline <span class="required">*</span></label>
          <input
            v-model="formData.professionalHeadline"
            type="text"
            required
            placeholder="Senior Software Engineer | Full-Stack Developer"
          />
        </div>

        <div class="form-group">
          <label>Professional Summary <span class="required">*</span></label>
          <textarea
            v-model="formData.summary"
            rows="5"
            required
            placeholder="Write a compelling summary highlighting your experience, skills, and career achievements..."
          ></textarea>
        </div>
      </CardContent>
    </Card>

    <!-- Languages -->
    <Card class="form-card">
      <CardContent class="pt-6">
        <div class="section-header">
          <h3 class="form-section-title">Languages</h3>
          <Dialog
            :open="languageDialogOpen"
            @update:open="languageDialogOpen = $event"
          >
            <DialogTrigger>
              <Button size="sm" variant="outline"> + Add Language </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Add Language</DialogTitle>
                <DialogDescription>
                  Add a new language and your proficiency level.
                </DialogDescription>
              </DialogHeader>
              <form @submit="onLanguageSubmit" class="dialog-form">
                <FormField v-slot="{ componentField }" name="language">
                  <FormItem>
                    <FormLabel
                      >Language <span class="required">*</span></FormLabel
                    >
                    <FormInput
                      type="text"
                      placeholder="e.g., English, Spanish, Mandarin"
                      v-bind="componentField"
                    />
                    <FormMessage />
                  </FormItem>
                </FormField>

                <FormField v-slot="{ componentField }" name="proficiency">
                  <FormItem>
                    <FormLabel
                      >Proficiency <span class="required">*</span></FormLabel
                    >
                    <select
                      v-bind="componentField"
                      class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    >
                      <option value="Basic">Basic</option>
                      <option value="Conversational">Conversational</option>
                      <option value="Professional">Professional</option>
                      <option value="Native">Native</option>
                    </select>
                    <FormMessage />
                  </FormItem>
                </FormField>

                <DialogFooter>
                  <Button
                    @click="languageDialogOpen = false"
                    variant="outline"
                    type="button"
                  >
                    Cancel
                  </Button>
                  <Button type="submit"> Add Language </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <!-- Languages List -->
        <div v-if="formData.languages.length > 0" class="languages-list">
          <div
            v-for="(lang, index) in formData.languages"
            :key="index"
            class="language-item"
          >
            <div class="language-info">
              <span class="language-name">{{ lang.language }}</span>
              <span class="language-proficiency">{{ lang.proficiency }}</span>
            </div>
            <Button
              @click="removeLanguage(index)"
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
        <div v-else class="empty-state">
          <p>No languages added yet. Click "Add Language" to get started.</p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, watch } from "vue";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";
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
import {
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormInput,
} from "@/components/ui/form";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue"]);

const formData = props.modelValue;

const languageDialogOpen = ref(false);

// Zod schema for language form
const languageSchema = toTypedSchema(
  z.object({
    language: z.string().min(1, "Language is required"),
    proficiency: z.enum(["Basic", "Conversational", "Professional", "Native"]),
  })
);

const { handleSubmit, resetForm, setValues, setTouched } = useForm({
  validationSchema: languageSchema,
  initialValues: {
    language: "",
    proficiency: "Professional",
  },
  validateOnMount: false,
});

// Reset form state when dialog opens
watch(languageDialogOpen, (isOpen) => {
  if (isOpen) {
    resetForm();
  }
});

const onLanguageSubmit = handleSubmit(
  (values) => {
    formData.languages.push({
      language: values.language,
      proficiency: values.proficiency,
    });
    resetForm();
    languageDialogOpen.value = false;
  },
  (validationErrors) => {
    // On validation failure, mark all error fields as touched
    Object.keys(validationErrors.errors).forEach((field) => {
      setTouched(field, true);
    });
  }
);

function removeLanguage(index) {
  formData.languages.splice(index, 1);
}

function fillDummyData() {
  // Personal Information
  formData.personalInfo.firstName = "Sarah";
  formData.personalInfo.lastName = "Chen";
  formData.personalInfo.email = "sarah.chen@email.com";
  formData.personalInfo.phone = "+1 (415) 555-0123";
  formData.personalInfo.location.city = "San Francisco";
  formData.personalInfo.location.state = "CA";
  formData.personalInfo.location.country = "United States";
  formData.personalInfo.linkedinUrl = "https://linkedin.com/in/sarahchen";
  formData.personalInfo.portfolioUrl = "https://sarahchen.dev";

  // Professional Headline
  formData.professionalHeadline =
    "Senior Full-Stack Developer | React & Node.js Specialist | Cloud Architecture Expert";

  // Professional Summary
  formData.summary =
    "Innovative Full-Stack Developer with 8+ years of experience building scalable web applications and leading engineering teams. Specialized in React, Node.js, and cloud-native architectures. Proven track record of delivering high-impact projects that improve user experience and drive business growth. Passionate about clean code, mentoring junior developers, and staying current with emerging technologies.";

  // Languages
  formData.languages = [
    { language: "English", proficiency: "Native" },
    { language: "Mandarin Chinese", proficiency: "Professional" },
    { language: "Spanish", proficiency: "Conversational" },
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
  margin: 0 0 20px 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* Dialog Form */
.dialog-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 0;
}

/* Languages List */
.languages-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.language-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
  border-bottom: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.language-item:last-child {
  border-bottom: none;
}

.language-item:hover {
  opacity: 0.8;
}

.language-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.language-name {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
  min-width: 150px;
}

.language-proficiency {
  font-size: 14px;
  color: #64748b;
  padding: 4px 12px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
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
  padding: 32px;
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  background: #f9fafb;
  border: 1px dashed #e5e7eb;
  border-radius: 8px;
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

.repeatable-item {
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 12px;
  position: relative;
}

.repeatable-item .form-row {
  align-items: flex-end;
  margin-bottom: 0;
}

.remove-btn {
  flex-shrink: 0;
  color: #ef4444;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
