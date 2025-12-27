<template>
  <div class="job-description-input">
    <h2>Job Description</h2>
    <textarea
      v-model="jobDescription"
      @input="$emit('update:modelValue', jobDescription)"
      rows="10"
      placeholder="Paste the job description here..."
      required
    ></textarea>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const jobDescription = ref(props.modelValue)
</script>

<style scoped>
.job-description-input {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  background: #f9f9f9;
  margin-top: 20px;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
}
</style>
