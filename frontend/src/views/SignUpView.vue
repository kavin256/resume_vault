<template>
  <div class="signup-view">
    <div class="signup-container">
      <div class="signup-header">
        <h1 class="signup-title">Create Your Account</h1>
        <p class="signup-description">
          Join Resume Vault and start generating tailored resumes in minutes
        </p>
      </div>
      <div class="clerk-signup-wrapper">
        <SignUp :sign-in-url="'/sign-in'" :after-sign-up-url="'/home'" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { SignUp } from "@clerk/vue";
</script>

<style scoped>
.signup-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%);
  padding: 40px 20px;
}

.signup-container {
  width: 100%;
  max-width: 480px;
}

.signup-header {
  text-align: center;
  margin-bottom: 32px;
}

.signup-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
}

.signup-description {
  font-size: 15px;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

.clerk-signup-wrapper {
  display: flex;
  justify-content: center;
}

@media (max-width: 600px) {
  .signup-title {
    font-size: 24px;
  }

  .signup-description {
    font-size: 14px;
  }
}
</style>
