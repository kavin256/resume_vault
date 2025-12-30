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
              <Button class="add-language-btn" size="sm">
                + Add Language
              </Button>
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
                    :disabled="isSavingLanguage"
                  >
                    Cancel
                  </Button>
                  <Button type="submit" :disabled="isSavingLanguage">
                    {{ isSavingLanguage ? "Adding..." : "Add Language" }}
                  </Button>
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

const auth = useAuth();
const formData = props.modelValue;

const languageDialogOpen = ref(false);
const isSavingLanguage = ref(false);

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
  async (values) => {
    isSavingLanguage.value = true;
    try {
      // Add language to local data
      formData.languages.push({
        language: values.language,
        proficiency: values.proficiency,
      });

      // Save to database immediately
      const token = await auth.getToken.value();
      if (token) {
        await updateMasterProfile(token, {
          languages: formData.languages,
        });
        console.log("[PersonalInfoStep] Language added and saved to database");
      }

      resetForm();
      languageDialogOpen.value = false;
    } catch (error) {
      console.error("[PersonalInfoStep] Failed to save language:", error);
      // Remove the language from local data if save failed
      formData.languages.pop();
      alert("Failed to save language. Please try again.");
    } finally {
      isSavingLanguage.value = false;
    }
  },
  (validationErrors) => {
    // On validation failure, mark all error fields as touched
    Object.keys(validationErrors.errors).forEach((field) => {
      setTouched(field, true);
    });
  }
);

async function removeLanguage(index) {
  const removedLanguage = formData.languages[index];

  // Remove from local data
  formData.languages.splice(index, 1);

  try {
    // Save to database immediately
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, {
        languages: formData.languages,
      });
      console.log("[PersonalInfoStep] Language removed and saved to database");
    }
  } catch (error) {
    console.error("[PersonalInfoStep] Failed to remove language:", error);
    // Restore the language if save failed
    formData.languages.splice(index, 0, removedLanguage);
    alert("Failed to remove language. Please try again.");
  }
}

async function fillDummyData() {
  try {
    console.log("[PersonalInfoStep] Filling with test data");

    const dummyData = {
      personalInfo: {
        firstName: "Sarah",
        lastName: "Chen",
        email: "sarah.chen@email.com",
        phone: "+1 (415) 555-0123",
        location: {
          city: "San Francisco",
          state: "CA",
          country: "United States",
        },
        linkedinUrl: "https://linkedin.com/in/sarahchen",
        portfolioUrl: "https://sarahchen.dev",
      },
      professionalHeadline:
        "Senior Full-Stack Developer | React & Node.js Specialist | Cloud Architecture Expert",
      summary:
        "Innovative Full-Stack Developer with 8+ years of experience building scalable web applications and leading engineering teams. Specialized in React, Node.js, and cloud-native architectures. Proven track record of delivering high-impact projects that improve user experience and drive business growth. Passionate about clean code, mentoring junior developers, and staying current with emerging technologies.",
      languages: [
        { language: "English", proficiency: "Native" },
        { language: "Mandarin Chinese", proficiency: "Professional" },
        { language: "Spanish", proficiency: "Conversational" },
      ],
    };

    // Save directly to database
    const token = await auth.getToken.value();
    if (token) {
      await updateMasterProfile(token, dummyData);
      console.log("[PersonalInfoStep] Test data saved to database");

      // Update local state to reflect saved data
      Object.assign(formData.personalInfo, dummyData.personalInfo);
      formData.professionalHeadline = dummyData.professionalHeadline;
      formData.summary = dummyData.summary;
      formData.languages = dummyData.languages;

      alert("Test data filled and saved successfully!");
    }
  } catch (error) {
    console.error("[PersonalInfoStep] Error filling test data:", error);
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
  margin-bottom: 24px;
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

.form-section-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 20px 0;
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
  gap: 12px;
  flex-wrap: wrap;
}

@media (max-width: 640px) {
  .section-header {
    flex-direction: column;
    align-items: stretch;
  }

  .section-header .form-section-title {
    width: 100%;
  }
}

.add-language-btn {
  background: white;
  color: #667eea;
  border: 2px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  font-weight: 500;
  padding: 10px 20px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
}

.add-language-btn:hover {
  background-image: linear-gradient(135deg, #f8f9ff 0%, #faf8ff 100%), linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
  color: #5568d3;
}

@media (max-width: 640px) {
  .add-language-btn {
    width: 100%;
    justify-content: center;
  }
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
  background-image: linear-gradient(white, white), linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  font-weight: 500;
  transition: all 0.3s ease;
}

.dialog-form button[variant="outline"]:hover {
  background-image: linear-gradient(135deg, #f8f9ff 0%, #faf8ff 100%), linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translateY(-2px);
  color: #5568d3;
}

/* Languages List */
.languages-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-top: 8px;
}

.language-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
  gap: 16px;
}

.language-item:first-child {
  border-radius: 12px 12px 0 0;
}

.language-item:last-child {
  border-bottom: none;
  border-radius: 0 0 12px 12px;
}

.language-item:only-child {
  border-radius: 12px;
}

.language-item:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transform: translateX(4px);
}

@media (max-width: 640px) {
  .language-item {
    flex-direction: column;
    align-items: flex-start;
    padding: 16px;
    gap: 12px;
  }
}

.language-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
  flex-wrap: wrap;
}

@media (max-width: 640px) {
  .language-info {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}

.language-name {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
  min-width: 150px;
}

@media (max-width: 640px) {
  .language-name {
    min-width: auto;
    font-size: 14px;
  }
}

.language-proficiency {
  font-size: 14px;
  color: #667eea;
  padding: 6px 14px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.language-proficiency:hover {
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  border-color: #c7d2fe;
}

@media (max-width: 640px) {
  .language-proficiency {
    font-size: 13px;
    padding: 4px 12px;
  }
}

.delete-btn {
  color: #ef4444;
  padding: 8px;
  height: auto;
  min-width: 40px;
  transition: all 0.2s ease;
  border-radius: 8px;
}

.delete-btn:hover {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #dc2626;
  transform: scale(1.05);
}

@media (max-width: 640px) {
  .delete-btn {
    align-self: flex-end;
    width: 100%;
    justify-content: center;
  }
}

.empty-state {
  padding: 40px 32px;
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 2px dashed #e2e8f0;
  border-radius: 12px;
  margin-top: 8px;
  transition: all 0.3s ease;
}

.empty-state:hover {
  border-color: #cbd5e1;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

@media (max-width: 640px) {
  .empty-state {
    padding: 32px 20px;
    font-size: 13px;
  }
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
