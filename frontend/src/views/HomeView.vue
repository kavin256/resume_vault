<template>
  <div class="home-view">
    <div class="page-header">
      <h1>Vault</h1>
      <p class="page-description">
        Welcome — manage your master profile and generate tailored resumes.
      </p>
    </div>

    <!-- Summary stats -->
    <div class="stats-grid">
      <Card>
        <CardContent class="pt-6">
          <div class="stat-value">{{ applications.length }}</div>
          <div class="stat-label">Total Applications</div>
        </CardContent>
      </Card>

      <Card>
        <CardContent class="pt-6">
          <div class="stat-value">{{ recentApplications }}</div>
          <div class="stat-label">Recent (Last 30 Days)</div>
        </CardContent>
      </Card>

      <Card>
        <CardContent class="pt-6">
          <div class="stat-value">{{ applications.length }}</div>
          <div class="stat-label">Companies Applied</div>
        </CardContent>
      </Card>
    </div>

    <!-- Recent application history -->
    <Card>
      <CardContent class="pt-6">
        <h2 class="section-title">Recent Applications</h2>
        <DataTable
          :columns="columns"
          :data="applications"
          search-key="company"
          filter-label="Search by company..."
        />
      </CardContent>
    </Card>

    <!-- Drawer using shadcn-vue Sheet -->
    <Sheet v-model:open="drawerOpen">
      <SheetContent
        :side="drawerSide"
        :class="drawerSide === 'bottom' ? 'h-[85vh]' : 'sm:max-w-[540px]'"
        class="overflow-y-auto"
      >
        <SheetHeader>
          <SheetTitle>Application Details</SheetTitle>
          <SheetDescription>
            View details of your job application
          </SheetDescription>
        </SheetHeader>

        <div class="drawer-content" v-if="selectedApp">
          <!-- Job Details -->
          <div class="drawer-section">
            <h4 class="drawer-section-title">Job Details</h4>
            <div class="detail-row">
              <span class="detail-label">Company</span>
              <span class="detail-value">{{ selectedApp.company }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Position</span>
              <span class="detail-value">{{ selectedApp.position }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Job ID</span>
              <span class="detail-value">{{ selectedApp.jobId }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Posting Link</span>
              <a
                :href="selectedApp.postingLink"
                target="_blank"
                class="detail-link"
                >View Posting →</a
              >
            </div>
          </div>

          <!-- Job Description -->
          <div class="drawer-section">
            <h4 class="drawer-section-title">Job Description</h4>
            <div class="job-description">{{ selectedApp.jobDescription }}</div>
          </div>

          <!-- Date Generated -->
          <div class="drawer-section">
            <h4 class="drawer-section-title">Generation Info</h4>
            <div class="detail-row">
              <span class="detail-label">Date Generated</span>
              <span class="detail-value">{{ selectedApp.dateGenerated }}</span>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, h } from "vue";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import DataTable from "@/components/DataTable.vue";
import { ArrowUpDown } from "lucide-vue-next";
import { useUserSync } from "@/composables/useUserSync";

const drawerOpen = ref(false);
const selectedApp = ref(null);
const windowWidth = ref(window.innerWidth);

// User sync
const { performUserSync } = useUserSync();

// Update window width on resize
const updateWidth = () => {
  windowWidth.value = window.innerWidth;
};

onMounted(() => {
  window.addEventListener("resize", updateWidth);

  // Sync user with backend on component mount
  performUserSync();
});

onUnmounted(() => {
  window.removeEventListener("resize", updateWidth);
});

// Responsive drawer side: bottom for mobile, right for desktop
const drawerSide = computed(() => {
  return windowWidth.value < 768 ? "bottom" : "right";
});

// Dummy application data
const applications = [
  {
    id: 1,
    company: "TechCorp Inc.",
    position: "Senior Full-Stack Engineer",
    status: "Applied",
    appliedDate: "2025-12-15",
    jobId: "REQ-2024-SE-4567",
    postingLink: "https://techcorp.com/careers/senior-fullstack-engineer-4567",
    jobDescription: `We are seeking an experienced Senior Full-Stack Software Engineer to join our growing engineering team. You will be responsible for designing, developing, and maintaining scalable web applications that serve millions of users worldwide.

Key Responsibilities:
• Design and implement robust, scalable backend services
• Build responsive, performant frontend applications
• Collaborate with product managers and designers
• Write clean, maintainable code with comprehensive test coverage
• Participate in code reviews and mentor junior engineers

Required Qualifications:
• 5+ years of professional software development experience
• Strong proficiency in JavaScript/TypeScript and Python
• Experience with modern frontend frameworks (React, Vue.js, or Angular)
• Solid understanding of backend technologies (Node.js, FastAPI, Django)`,
    dateGenerated: "2025-12-15",
  },
  {
    id: 2,
    company: "InnovateLab",
    position: "Frontend Engineer",
    status: "Interview",
    appliedDate: "2025-11-28",
    jobId: "JOB-2024-FE-123",
    postingLink: "https://innovatelab.com/careers/frontend-engineer",
    jobDescription: `Join our frontend team to build beautiful, responsive user interfaces using modern web technologies. You'll work closely with designers to bring creative visions to life.

Requirements:
• 3+ years of frontend development experience
• Expert knowledge of React or Vue.js
• Strong CSS and responsive design skills
• Experience with state management libraries`,
    dateGenerated: "2025-11-28",
  },
  {
    id: 3,
    company: "StartupCo",
    position: "Backend Engineer",
    status: "Rejected",
    appliedDate: "2025-10-05",
    jobId: "HIRE-2024-BE-789",
    postingLink: "https://startupco.com/jobs/backend-engineer",
    jobDescription: `We're looking for a talented backend engineer to help us scale our infrastructure and build robust APIs. You'll be working on challenging problems in distributed systems.

What you'll do:
• Design and build scalable microservices
• Optimize database performance
• Implement secure authentication and authorization
• Deploy and monitor production systems`,
    dateGenerated: "2025-10-05",
  },
  {
    id: 4,
    company: "CloudSystems",
    position: "DevOps Engineer",
    status: "Applied",
    appliedDate: "2025-12-10",
    jobId: "CLOUD-2024-DEV-456",
    postingLink: "https://cloudsystems.com/careers/devops",
    jobDescription:
      "Build and maintain cloud infrastructure, CI/CD pipelines, and monitoring systems.",
    dateGenerated: "2025-12-10",
  },
  {
    id: 5,
    company: "DataTech Solutions",
    position: "Data Engineer",
    status: "Interview",
    appliedDate: "2025-11-15",
    jobId: "DATA-2024-ENG-321",
    postingLink: "https://datatech.com/jobs/data-engineer",
    jobDescription:
      "Design and implement data pipelines, ETL processes, and data warehousing solutions.",
    dateGenerated: "2025-11-15",
  },
];

// Calculate recent applications (last 30 days)
const recentApplications = computed(() => {
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  return applications.filter(
    (app) => new Date(app.appliedDate) >= thirtyDaysAgo
  ).length;
});

// Define table columns
const columns = [
  {
    accessorKey: "company",
    header: ({ column }) => {
      return h(
        Button,
        {
          variant: "ghost",
          onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        },
        () => ["Company", h(ArrowUpDown, { class: "ml-2 h-4 w-4" })]
      );
    },
    cell: ({ row }) =>
      h("div", { class: "font-medium" }, row.getValue("company")),
  },
  {
    accessorKey: "position",
    header: "Position",
    cell: ({ row }) => h("div", row.getValue("position")),
  },
  {
    accessorKey: "appliedDate",
    header: ({ column }) => {
      return h(
        Button,
        {
          variant: "ghost",
          onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
        },
        () => ["Date Applied", h(ArrowUpDown, { class: "ml-2 h-4 w-4" })]
      );
    },
    cell: ({ row }) => h("div", row.getValue("appliedDate")),
  },
  {
    id: "actions",
    header: "Actions",
    cell: ({ row }) => {
      const app = row.original;
      return h(
        Button,
        {
          variant: "outline",
          size: "sm",
          onClick: () => openDrawer(app),
        },
        () => "Details"
      );
    },
  },
];

function openDrawer(app) {
  selectedApp.value = app;
  drawerOpen.value = true;
}
</script>

<style scoped>
.home-view {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 48px 64px 48px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}

.page-description {
  font-size: 16px;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

/* Stats grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

/* Applications section */
.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 16px 0;
}

/* Drawer content */
.drawer-content {
  padding-top: 24px;
}

.drawer-section {
  margin-bottom: 32px;
}

.drawer-section:last-child {
  margin-bottom: 0;
}

.drawer-section-title {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 16px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
  flex-shrink: 0;
  width: 120px;
}

.detail-value {
  font-size: 14px;
  color: #0f172a;
  text-align: right;
  flex: 1;
}

.detail-link {
  font-size: 14px;
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.15s ease;
}

.detail-link:hover {
  color: #2563eb;
  text-decoration: underline;
}

.job-description {
  font-size: 14px;
  color: #334155;
  line-height: 1.7;
  white-space: pre-line;
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

@media (max-width: 900px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .app-row {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  .app-date {
    justify-self: start;
  }
}
</style>
