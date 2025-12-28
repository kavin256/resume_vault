<template>
  <nav class="app-nav" :class="{ 'mobile-open': mobileMenuOpen }">
    <!-- Mobile Header -->
    <div class="mobile-header">
      <div class="nav-brand">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"
          ></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
        <span class="brand-text">Resume Vault</span>
      </div>
      <Button
        @click="toggleMobileMenu"
        variant="ghost"
        size="icon"
        aria-label="Toggle menu"
      >
        <svg
          v-if="!mobileMenuOpen"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg
          v-else
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </Button>
    </div>

    <!-- Sidebar Navigation -->
    <div class="nav-sidebar">
      <div class="nav-brand-desktop">
        <svg
          width="28"
          height="28"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"
          ></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
        <span class="brand-text">Resume Vault</span>
      </div>

      <div class="nav-links">
        <router-link to="/home" class="nav-link" @click="closeMobileMenu">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M3 11l9-7 9 7v8a2 2 0 0 1-2 2h-4V13H9v8H5a2 2 0 0 1-2-2v-8z"
            ></path>
          </svg>
          <span>Vault</span>
        </router-link>
        <router-link to="/profile" class="nav-link" @click="closeMobileMenu">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <span>Master Profile</span>
        </router-link>
        <router-link to="/generate" class="nav-link" @click="closeMobileMenu">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"
            ></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          <span>Generate Resume</span>
        </router-link>
      </div>

      <!-- User Profile Section -->
      <div class="nav-footer">
        <div class="user-section" v-if="user" @click="handleUserClick">
          <div class="user-info">
            <div class="user-avatar">
              <img
                v-if="user.imageUrl"
                :src="user.imageUrl"
                :alt="displayName"
                class="avatar-image"
              />
              <svg
                v-else
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                class="avatar-icon"
              >
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div class="user-details">
              <div class="user-name">{{ displayName }}</div>
              <div class="user-email" v-if="user.primaryEmailAddress">
                {{ user.primaryEmailAddress.emailAddress }}
              </div>
            </div>
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="chevron-icon"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>
          <div class="user-button-hidden">
            <UserButton :after-sign-out-url="'/'" />
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from "vue";
import { Button } from "@/components/ui/button";
import { UserButton, useUser } from "@clerk/vue";

const mobileMenuOpen = ref(false);
const { user } = useUser();

const displayName = computed(() => {
  if (!user.value) return "";

  const firstName = user.value.firstName;
  const lastName = user.value.lastName;

  if (firstName && lastName) {
    return `${firstName} ${lastName}`;
  } else if (firstName) {
    return firstName;
  } else if (lastName) {
    return lastName;
  } else if (user.value.primaryEmailAddress) {
    return user.value.primaryEmailAddress.emailAddress;
  }

  return "User";
});

function handleUserClick() {
  // Trigger click on the hidden UserButton
  const userButton = document.querySelector(".user-button-hidden button");
  if (userButton) {
    userButton.click();
  }
}

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value;
}

function closeMobileMenu() {
  mobileMenuOpen.value = false;
}
</script>

<style scoped>
/* Mobile Header (hidden on desktop) */
.mobile-header {
  display: none;
}

/* Desktop Sidebar */
.app-nav {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 260px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.04);
  z-index: 100;
  overflow-y: auto;
}

.nav-sidebar {
  display: flex;
  flex-direction: column;
  padding: 32px 0;
  height: 100%;
}

.nav-brand-desktop {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #0f172a;
  padding: 0 24px;
  margin-bottom: 40px;
}

.nav-brand-desktop svg {
  flex-shrink: 0;
  color: #3b82f6;
}

.brand-text {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 16px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  font-size: 15px;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.15s ease;
}

.nav-link svg {
  flex-shrink: 0;
  color: currentColor;
}

.nav-link:hover {
  color: #0f172a;
  background: #f8fafc;
}

.nav-link.router-link-active {
  color: #3b82f6;
  background: #eff6ff;
}

/* User Footer Section */
.nav-footer {
  margin-top: auto;
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
}

.user-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  background: #f8fafc;
  border-radius: 8px;
  transition: all 0.15s ease;
}

.user-section:hover .user-info {
  background: #e5e7eb;
}

.user-button-hidden {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  z-index: -1;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-icon {
  color: #64748b;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 12px;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chevron-icon {
  color: #64748b;
  flex-shrink: 0;
  margin-left: auto;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .app-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: auto;
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  }

  .mobile-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    background: #ffffff;
  }

  .nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #0f172a;
  }

  .nav-brand svg {
    flex-shrink: 0;
    color: #3b82f6;
  }

  .nav-sidebar {
    display: none;
    padding: 16px 0 24px;
  }

  .app-nav.mobile-open .nav-sidebar {
    display: flex;
  }

  .nav-brand-desktop {
    display: none;
  }

  .nav-links {
    padding: 0 20px;
  }

  .brand-text {
    font-size: 18px;
  }
}
</style>
