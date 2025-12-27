<template>
  <div class="master-profile-form">
    <h2>Master Profile</h2>
    <form @submit.prevent>
      <div class="form-group">
        <label>Name:</label>
        <input v-model="profile.name" type="text" required />
      </div>

      <div class="form-group">
        <label>Email:</label>
        <input v-model="profile.email" type="email" required />
      </div>

      <div class="form-group">
        <label>Phone:</label>
        <input v-model="profile.phone" type="tel" required />
      </div>

      <div class="form-group">
        <label>Experience:</label>
        <textarea v-model="profile.experience" rows="3" required></textarea>
      </div>

      <div class="form-group">
        <label>Skills:</label>
        <input v-model="profile.skills" type="text" required />
      </div>

      <div class="form-group">
        <label>Education:</label>
        <input v-model="profile.education" type="text" required />
      </div>
    </form>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  profile: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.master-profile-form {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  background: #f9f9f9;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit;
}
</style>
