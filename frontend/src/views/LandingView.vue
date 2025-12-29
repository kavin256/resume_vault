<template>
  <div class="landing-view">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Resume Vault</h1>
        <p class="hero-subtitle">Your personal resume generation assistant</p>
        <p class="hero-description">
          Create tailored resumes and cover letters in seconds. Stop manually
          editing your resume for every job application—let Resume Vault do the
          work for you.
        </p>
        <Button size="lg" class="cta-button" @click="goToAuth">
          Get Started →
        </Button>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section">
      <h2 class="section-title">How It Works</h2>
      <div class="features-grid">
        <Card class="feature-card">
          <CardContent class="pt-6">
            <div class="feature-icon">📝</div>
            <h3 class="feature-title">Build Your Master Profile</h3>
            <p class="feature-description">
              Store all your professional information in one place—work
              experience, skills, education, and accomplishments.
            </p>
          </CardContent>
        </Card>

        <Card class="feature-card">
          <CardContent class="pt-6">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Paste Job Description</h3>
            <p class="feature-description">
              Simply copy the job posting you're interested in and paste it into
              Resume Vault. That's all you need to do.
            </p>
          </CardContent>
        </Card>

        <Card class="feature-card">
          <CardContent class="pt-6">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">Generate Instantly</h3>
            <p class="feature-description">
              Get a professionally tailored resume and cover letter as
              downloadable PDFs, ready to submit in seconds.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Benefits Section -->
    <div class="benefits-section">
      <h2 class="section-title">Why Choose Resume Vault?</h2>
      <div class="benefits-grid">
        <div class="benefit-item">
          <div class="benefit-icon">⏱️</div>
          <div class="benefit-content">
            <h3 class="benefit-title">Save Time</h3>
            <p class="benefit-text">
              No more manual resume editing for every application. Generate
              tailored documents in seconds.
            </p>
          </div>
        </div>

        <div class="benefit-item">
          <div class="benefit-icon">📂</div>
          <div class="benefit-content">
            <h3 class="benefit-title">Stay Organized</h3>
            <p class="benefit-text">
              Keep all your professional information in one master profile.
              Update once, use everywhere.
            </p>
          </div>
        </div>

        <div class="benefit-item">
          <div class="benefit-icon">✨</div>
          <div class="benefit-content">
            <h3 class="benefit-title">Professional Output</h3>
            <p class="benefit-text">
              Generate polished PDF documents with clean formatting, ready to
              submit to employers.
            </p>
          </div>
        </div>

        <div class="benefit-item">
          <div class="benefit-icon">🚀</div>
          <div class="benefit-content">
            <h3 class="benefit-title">Easy Workflow</h3>
            <p class="benefit-text">
              Simple two-step process: create your profile, then generate
              documents. No complexity.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="cta-section">
      <Card class="cta-card">
        <CardContent class="pt-8 pb-8">
          <h2 class="cta-title">Ready to streamline your job search?</h2>
          <p class="cta-description">
            Join thousands of job seekers who save hours on every application.
          </p>
          <Button size="lg" class="cta-button-secondary" @click="goToAuth">
            Sign Up Free →
          </Button>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuth } from "@clerk/vue";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const router = useRouter();
const { isSignedIn } = useAuth();

function goToAuth() {
  // If user is already signed in, go to home, otherwise go to sign-in
  if (isSignedIn.value) {
    router.push("/home");
  } else {
    router.push("/sign-in");
  }
}
</script>

<style scoped>
.landing-view {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%);
}

/* Hero Section */
.hero-section {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 85vh;
  padding: 80px 24px 60px 24px;
  text-align: center;
}

.hero-content {
  max-width: 720px;
}

.hero-title {
  font-size: 64px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 20px 0;
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.hero-subtitle {
  font-size: 24px;
  font-weight: 500;
  color: #475569;
  margin: 0 0 20px 0;
  line-height: 1.4;
}

.hero-description {
  font-size: 18px;
  color: #64748b;
  margin: 0 0 40px 0;
  line-height: 1.7;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-button {
  font-size: 18px;
  padding: 24px 48px;
  height: auto;
  font-weight: 600;
}

/* Features Section */
.features-section {
  padding: 80px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 40px;
  font-weight: 700;
  color: #0f172a;
  text-align: center;
  margin: 0 0 60px 0;
  letter-spacing: -0.02em;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.feature-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature-title {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 12px 0;
}

.feature-description {
  font-size: 15px;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

/* Benefits Section */
.benefits-section {
  padding: 80px 24px;
  max-width: 1000px;
  margin: 0 auto;
  background: #ffffff;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
}

.benefit-item {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.benefit-icon {
  font-size: 36px;
  flex-shrink: 0;
}

.benefit-content {
  flex: 1;
}

.benefit-title {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.benefit-text {
  font-size: 15px;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

/* CTA Section */
.cta-section {
  padding: 80px 24px 100px 24px;
  max-width: 800px;
  margin: 0 auto;
}

.cta-card {
  text-align: center;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
  color: white;
}

.cta-title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 16px 0;
  letter-spacing: -0.02em;
}

.cta-description {
  font-size: 18px;
  color: #e0e7ff;
  margin: 0 0 32px 0;
  line-height: 1.6;
}

.cta-button-secondary {
  font-size: 18px;
  padding: 24px 48px;
  height: auto;
  font-weight: 600;
  background: #ffffff;
  color: #2563eb;
}

.cta-button-secondary:hover {
  background: #f1f5f9;
}

/* Responsive Design */
@media (max-width: 900px) {
  .hero-title {
    font-size: 48px;
  }

  .hero-subtitle {
    font-size: 20px;
  }

  .hero-description {
    font-size: 16px;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .benefits-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .section-title {
    font-size: 32px;
  }

  .cta-title {
    font-size: 28px;
  }

  .cta-button,
  .cta-button-secondary {
    font-size: 16px;
    padding: 20px 40px;
  }
}

@media (max-width: 600px) {
  .hero-section {
    min-height: 70vh;
    padding: 60px 20px 40px 20px;
  }

  .hero-title {
    font-size: 40px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .features-section,
  .benefits-section {
    padding: 60px 20px;
  }

  .cta-section {
    padding: 60px 20px 80px 20px;
  }
}
</style>
