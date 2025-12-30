<template>
  <div class="billing-view">
    <div class="billing-container">
      <!-- Page Header -->
      <div class="page-header">
        <h1>Billing & Subscription</h1>
        <p class="page-description">
          Manage your subscription and view your usage statistics
        </p>
      </div>

      <!-- Current Plan Card -->
      <Card class="current-plan-card">
        <CardContent class="pt-6">
          <div class="plan-header">
            <div class="plan-info">
              <div class="plan-badge-container">
                <h2 class="plan-name">{{ currentPlan.name }}</h2>
              </div>
              <p class="plan-price">
                ${{ currentPlan.price }}
                <span class="billing-cycle"
                  >/{{ currentPlan.billingCycle }}</span
                >
              </p>
            </div>
            <Button class="upgrade-btn" v-if="canUpgrade">
              Upgrade Plan
            </Button>
          </div>

          <!-- Usage Metrics -->
          <div class="usage-metrics">
            <div class="metric-card">
              <div class="metric-icon pdf-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
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
              <div class="metric-info">
                <p class="metric-label">PDF Generations</p>
                <p class="metric-value">
                  {{ usage.pdfGenerations }} /
                  {{ currentPlan.limits.pdfGenerations }}
                </p>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{
                      width: `${
                        (usage.pdfGenerations /
                          currentPlan.limits.pdfGenerations) *
                        100
                      }%`,
                    }"
                  ></div>
                </div>
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon letter-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <rect width="20" height="16" x="2" y="4" rx="2" />
                  <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
                </svg>
              </div>
              <div class="metric-info">
                <p class="metric-label">Cover Letters</p>
                <p class="metric-value">
                  {{ usage.coverLetters }} /
                  {{ currentPlan.limits.coverLetters }}
                </p>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{
                      width: `${
                        (usage.coverLetters / currentPlan.limits.coverLetters) *
                        100
                      }%`,
                    }"
                  ></div>
                </div>
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon calendar-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
                  <line x1="16" x2="16" y1="2" y2="6" />
                  <line x1="8" x2="8" y1="2" y2="6" />
                  <line x1="3" x2="21" y1="10" y2="10" />
                </svg>
              </div>
              <div class="metric-info">
                <p class="metric-label">Renewal Date</p>
                <p class="metric-value-large">{{ renewalDate }}</p>
                <p class="metric-sublabel">
                  {{ daysUntilRenewal }} days remaining
                </p>
              </div>
            </div>

            <div class="metric-card">
              <div class="metric-icon tracking-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
              </div>
              <div class="metric-info">
                <p class="metric-label">Job Applications</p>
                <p class="metric-value">
                  {{ usage.jobTracking }} / {{ currentPlan.limits.jobTracking }}
                </p>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{
                      width: `${
                        (usage.jobTracking / currentPlan.limits.jobTracking) *
                        100
                      }%`,
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Pricing Tiers Section -->
      <div class="pricing-section">
        <div class="section-header">
          <h2 class="section-title">Choose Your Plan</h2>
          <p class="section-description">
            Select the plan that best fits your job search needs
          </p>
        </div>

        <div class="pricing-grid">
          <Card
            v-for="tier in pricingTiers"
            :key="tier.id"
            class="pricing-card"
            :class="{
              popular: tier.popular,
              current: tier.id === currentPlan.id,
            }"
          >
            <CardContent class="pricing-content">
              <!-- Popular Badge -->
              <div v-if="tier.popular" class="popular-tag">
                ⭐ {{ tier.badge }}
              </div>

              <!-- Current Plan Badge -->
              <div v-if="tier.id === currentPlan.id" class="current-plan-tag">
                Current Plan
              </div>

              <!-- Plan Header -->
              <div class="pricing-header">
                <h3 class="tier-name">{{ tier.name }}</h3>
                <div class="tier-price">
                  <span class="price-amount">${{ tier.price }}</span>
                  <span class="price-cycle">/{{ tier.billingCycle }}</span>
                </div>
              </div>

              <!-- Features List -->
              <ul class="features-list">
                <li v-for="(feature, index) in tier.features" :key="index">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="check-icon"
                  >
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                  {{ feature }}
                </li>
              </ul>

              <!-- Action Button -->
              <Button
                class="select-plan-btn"
                :class="{
                  current: tier.id === currentPlan.id,
                  upgrade: tier.id > currentPlan.id,
                }"
                :variant="tier.id === currentPlan.id ? 'outline' : 'default'"
                @click="selectPlan(tier)"
              >
                {{
                  tier.id === currentPlan.id
                    ? "Current Plan"
                    : tier.id < currentPlan.id
                    ? "Downgrade"
                    : "Upgrade Now"
                }}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- Billing History Section -->
      <Card class="billing-history-card">
        <CardContent class="pt-6">
          <h3 class="section-title">Billing History</h3>
          <div class="history-table">
            <div class="table-header">
              <span>Date</span>
              <span>Description</span>
              <span>Amount</span>
              <span>Status</span>
            </div>
            <div
              v-for="(transaction, index) in billingHistory"
              :key="index"
              class="table-row"
            >
              <span class="date">{{ transaction.date }}</span>
              <span class="description">{{ transaction.description }}</span>
              <span class="amount">${{ transaction.amount }}</span>
              <span class="status" :class="transaction.status.toLowerCase()">
                {{ transaction.status }}
              </span>
            </div>
            <div v-if="billingHistory.length === 0" class="empty-state">
              No billing history available
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import pricingData from "@/data/pricing-tiers.json";

// Load pricing tiers
const pricingTiers = ref(pricingData.tiers);

// Current plan (mock data - will come from API later)
const currentPlanId = ref(2); // Pro Job Hunter
const currentPlan = computed(() => {
  return pricingTiers.value.find((tier) => tier.id === currentPlanId.value);
});

const canUpgrade = computed(() => {
  return currentPlanId.value < pricingTiers.value.length - 1;
});

// Mock usage data (will come from API later)
const usage = ref({
  pdfGenerations: 45,
  coverLetters: 12,
  jobTracking: 87,
  resumeUploads: 8,
});

// Renewal date calculation (mock)
const subscriptionStartDate = new Date("2024-12-01");
const renewalDate = computed(() => {
  const renewal = new Date(subscriptionStartDate);
  renewal.setMonth(renewal.getMonth() + 1);
  return renewal.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
});

const daysUntilRenewal = computed(() => {
  const today = new Date();
  const renewal = new Date(subscriptionStartDate);
  renewal.setMonth(renewal.getMonth() + 1);
  const diff = Math.ceil((renewal - today) / (1000 * 60 * 60 * 24));
  return diff > 0 ? diff : 0;
});

// Mock billing history (will come from API later)
const billingHistory = ref([
  {
    date: "Dec 1, 2024",
    description: "Pro Job Hunter - Monthly Subscription",
    amount: "19.00",
    status: "Paid",
  },
  {
    date: "Nov 1, 2024",
    description: "Pro Job Hunter - Monthly Subscription",
    amount: "19.00",
    status: "Paid",
  },
  {
    date: "Oct 1, 2024",
    description: "Basic Job Seeker - Monthly Subscription",
    amount: "9.00",
    status: "Paid",
  },
]);

// Plan selection handler
function selectPlan(tier) {
  if (tier.id === currentPlanId.value) {
    return;
  }

  const action = tier.id > currentPlanId.value ? "upgrade" : "downgrade";
  if (
    confirm(
      `Are you sure you want to ${action} to ${tier.name} for $${tier.price}/${tier.billingCycle}?`
    )
  ) {
    // Here you would call an API to change the subscription
    console.log(`Selected plan: ${tier.name}`);
    alert(
      `Subscription change requested. You will be ${action}d to ${tier.name}.`
    );
  }
}
</script>

<style scoped>
.billing-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 40px 24px 80px 24px;
}

.billing-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 36px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 12px 0;
}

.page-description {
  font-size: 18px;
  color: #64748b;
  margin: 0;
}

/* Current Plan Card */
.current-plan-card {
  margin-bottom: 48px;
  border: 2px solid #e2e8f0;
  border-radius: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #e2e8f0;
}

.plan-badge-container {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.plan-name {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.popular-badge {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid #fbbf24;
}

.plan-price {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 8px 0 0 0;
}

.billing-cycle {
  font-size: 18px;
  color: #64748b;
  font-weight: 500;
}

.upgrade-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-weight: 600;
  padding: 12px 24px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.upgrade-btn:hover {
  background: linear-gradient(135deg, #5568d3 0%, #653a8a 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

/* Usage Metrics */
.usage-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.metric-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
}

.metric-info {
  flex: 1;
}

.metric-label {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin: 0 0 4px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.metric-value-large {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 4px 0;
}

.metric-sublabel {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

/* Pricing Section */
.pricing-section {
  margin-bottom: 48px;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 12px 0;
}

.section-description {
  font-size: 16px;
  color: #64748b;
  margin: 0;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.pricing-card {
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  transition: all 0.3s ease;
  background: white;
  position: relative;
  overflow: visible;
}

.pricing-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.pricing-card.popular {
  border-color: #667eea;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
}

.pricing-card.current {
  border-color: #10b981;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.pricing-content {
  padding: 28px 20px;
}

.popular-tag {
  position: absolute;
  top: -12px;
  right: 24px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  border: 2px solid #fbbf24;
}

.current-plan-tag {
  position: absolute;
  top: -12px;
  right: 24px;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  border: 2px solid #10b981;
}

.pricing-header {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e2e8f0;
}

.tier-name {
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 12px 0;
}

.tier-price {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-amount {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.price-cycle {
  font-size: 16px;
  color: #64748b;
  font-weight: 500;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
}

.features-list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 0;
  font-size: 14px;
  color: #475569;
  line-height: 1.5;
}

.check-icon {
  color: #10b981;
  flex-shrink: 0;
  margin-top: 2px;
}

.select-plan-btn {
  width: 100%;
  padding: 12px 24px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.select-plan-btn.upgrade {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.select-plan-btn.upgrade:hover {
  background: linear-gradient(135deg, #5568d3 0%, #653a8a 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.select-plan-btn.current {
  background: white;
  color: #10b981;
  border: 2px solid #10b981;
}

/* Billing History */
.billing-history-card {
  border: 2px solid #e2e8f0;
  border-radius: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.history-table {
  margin-top: 20px;
}

.table-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  gap: 16px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  font-weight: 600;
  font-size: 13px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  gap: 16px;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  background: white;
}

.table-row:first-child {
  border-top: 1px solid #e2e8f0;
}

.table-row:last-child {
  border-bottom: 1px solid #e2e8f0;
}

.table-row:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border-color: #cbd5e1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.table-row .date {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.table-row .description {
  font-size: 14px;
  color: #0f172a;
  font-weight: 600;
}

.table-row .amount {
  font-size: 14px;
  color: #0f172a;
  font-weight: 700;
}

.table-row .status {
  font-size: 13px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 12px;
  text-align: center;
}

.status.paid {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
}

.status.pending {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
}

.status.failed {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
  font-size: 14px;
}

@media (max-width: 1024px) {
  .pricing-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .billing-view {
    padding: 24px 16px 64px 16px;
  }

  .page-header h1 {
    font-size: 28px;
  }

  .plan-header {
    flex-direction: column;
    gap: 16px;
  }

  .usage-metrics {
    grid-template-columns: 1fr;
  }

  .pricing-grid {
    grid-template-columns: 1fr;
  }

  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .table-header {
    display: none;
  }

  .table-row {
    padding: 16px;
  }

  .table-row span::before {
    content: attr(class) ": ";
    font-weight: 600;
    text-transform: capitalize;
    color: #64748b;
    display: inline-block;
    min-width: 100px;
  }
}
</style>
