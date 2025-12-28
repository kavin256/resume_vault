<template>
  <div class="signin-view">
    <div class="signin-container">
      <div class="signin-header">
        <h1 class="signin-title">Welcome to Resume Vault</h1>
        <p class="signin-description">
          Sign in to access your master profile and generate tailored resumes
        </p>
      </div>
      <div class="clerk-signin-wrapper">
        <SignIn :sign-up-url="'/sign-up'" :after-sign-in-url="'/home'" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { SignIn } from "@clerk/vue";
</script>

<style scoped>
.signin-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%);
  padding: 40px 20px;
}

.signin-container {
  width: 100%;
  max-width: 480px;
}

.signin-header {
  text-align: center;
  margin-bottom: 32px;
}

.signin-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
}

.signin-description {
  font-size: 15px;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

.clerk-signin-wrapper {
  display: flex;
  justify-content: center;
}

@media (max-width: 600px) {
  .signin-title {
    font-size: 24px;
  }

  .signin-description {
    font-size: 14px;
  }
}
</style>
