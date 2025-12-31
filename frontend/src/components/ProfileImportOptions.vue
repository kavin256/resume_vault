<template>
  <div class="import-options-container">
    <div class="import-header">
      <h2 class="import-title">Quick Start Your Profile</h2>
      <p class="import-description">
        Import your existing resume or LinkedIn profile
      </p>
    </div>

    <div class="import-options-grid">
      <!-- Resume Upload Option -->
      <Card class="import-option-card" :class="{ disabled: isProcessing }">
        <CardContent class="option-content">
          <div class="option-icon resume-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
              />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" x2="8" y1="13" y2="13" />
              <line x1="16" x2="8" y1="17" y2="17" />
              <line x1="10" x2="8" y1="9" y2="9" />
            </svg>
          </div>
          <h3 class="option-title">Upload Resume</h3>
          <p class="option-description">
            Upload PDF or DOCX file for AI-powered data extraction
          </p>
          <input
            ref="fileInput"
            type="file"
            accept=".pdf,.doc,.docx"
            @change="handleFileUpload"
            class="hidden-file-input"
            :disabled="isProcessing"
          />
          <Button
            @click="triggerFileUpload"
            class="option-button"
            :disabled="isProcessing"
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
              class="button-icon"
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" x2="12" y1="3" y2="15" />
            </svg>
            {{
              isProcessing && processingType === "resume"
                ? "Processing..."
                : "Upload Resume"
            }}
          </Button>
        </CardContent>
      </Card>

      <!-- LinkedIn Import Option -->
      <Card class="import-option-card" :class="{ disabled: isProcessing }">
        <CardContent class="option-content">
          <div class="option-icon linkedin-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"
              />
              <rect width="4" height="12" x="2" y="9" />
              <circle cx="4" cy="4" r="2" />
            </svg>
          </div>
          <h3 class="option-title">Import from LinkedIn</h3>
          <p class="option-description">
            Connect via OAuth to import your complete professional history
          </p>
          <Button
            @click="handleLinkedInImport"
            class="option-button linkedin-button"
            :disabled="isProcessing"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="button-icon"
            >
              <path
                d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
              />
            </svg>
            {{
              isProcessing && processingType === "linkedin"
                ? "Connecting..."
                : "Connect LinkedIn"
            }}
          </Button>
        </CardContent>
      </Card>
    </div>

    <!-- Skip Option -->
    <div class="skip-section">
      <Button @click="handleSkip" variant="ghost" class="skip-button">
        Skip for now
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from "vue";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const emit = defineEmits(["resume-upload", "linkedin-import", "skip"]);

const fileInput = ref(null);
const isProcessing = ref(false);
const processingType = ref(null);

function triggerFileUpload() {
  fileInput.value?.click();
}

async function handleFileUpload(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  // Validate file type
  const allowedTypes = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ];
  if (!allowedTypes.includes(file.type)) {
    alert("Please upload a PDF, DOC, or DOCX file.");
    return;
  }

  // Validate file size (10MB limit)
  const maxSize = 10 * 1024 * 1024;
  if (file.size > maxSize) {
    alert("File size must be less than 10MB.");
    return;
  }

  isProcessing.value = true;
  processingType.value = "resume";

  try {
    emit("resume-upload", file);
  } catch (error) {
    console.error("Error uploading file:", error);
    alert("Failed to upload file. Please try again.");
  } finally {
    // Reset after a delay to allow parent to handle
    setTimeout(() => {
      isProcessing.value = false;
      processingType.value = null;
      if (fileInput.value) {
        fileInput.value.value = "";
      }
    }, 500);
  }
}

function handleLinkedInImport() {
  isProcessing.value = true;
  processingType.value = "linkedin";

  try {
    emit("linkedin-import");
  } catch (error) {
    console.error("Error importing from LinkedIn:", error);
    alert("Failed to connect to LinkedIn. Please try again.");
  } finally {
    // Reset after a delay to allow parent to handle
    setTimeout(() => {
      isProcessing.value = false;
      processingType.value = null;
    }, 500);
  }
}

function handleSkip() {
  emit("skip");
}
</script>

<style scoped>
.import-options-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 20px 20px;
}

@media (max-width: 768px) {
  .import-options-container {
    padding: 16px;
  }
}

.import-header {
  text-align: center;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .import-header {
    margin-bottom: 16px;
  }
}

.import-title {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

@media (max-width: 768px) {
  .import-title {
    font-size: 20px;
  }
}

.import-description {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .import-description {
    font-size: 13px;
  }
}

.import-options-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

@media (max-width: 768px) {
  .import-options-grid {
    gap: 12px;
    margin-bottom: 12px;
  }
}

.import-option-card {
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  transition: all 0.3s ease;
  cursor: pointer;
  background: white;
}

.import-option-card:hover:not(.disabled) {
  border-color: #3b82f6;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12);
  transform: translateY(-4px);
}

.import-option-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.option-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

@media (max-width: 768px) {
  .option-content {
    padding: 16px;
  }
}

.option-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

@media (max-width: 768px) {
  .option-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    margin-bottom: 10px;
  }

  .option-icon svg {
    width: 24px;
    height: 24px;
  }
}

.resume-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.linkedin-icon {
  background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%);
  color: white;
}

.option-title {
  font-size: 17px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 8px 0;
}

@media (max-width: 768px) {
  .option-title {
    font-size: 16px;
  }
}

.option-description {
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
  margin: 0 0 16px 0;
}

@media (max-width: 768px) {
  .option-description {
    font-size: 12px;
    margin: 0 0 12px 0;
  }
}

.hidden-file-input {
  display: none;
}

.option-button {
  width: 100%;
  height: 40px;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
}

.option-button:hover {
  background: linear-gradient(135deg, #5568d3 0%, #653a8a 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
}

@media (max-width: 768px) {
  .option-button {
    height: 38px;
    font-size: 13px;
  }
}

.linkedin-button {
  background: linear-gradient(135deg, #0077b5 0%, #005582 100%);
}

.linkedin-button:hover {
  background: linear-gradient(135deg, #006399 0%, #004a6b 100%);
}

.button-icon {
  flex-shrink: 0;
}

.skip-section {
  text-align: center;
  padding: 12px 0 0;
}

@media (max-width: 768px) {
  .skip-section {
    padding: 8px 0 0;
  }
}

.skip-button {
  font-size: 13px;
  color: #667eea;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  transition: all 0.2s ease;
}

.skip-button:hover {
  color: #5568d3;
  background: linear-gradient(135deg, #f8f9ff 0%, #faf8ff 100%);
}

@media (max-width: 768px) {
  .skip-button {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>
