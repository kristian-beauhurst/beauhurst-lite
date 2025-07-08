<template>
  <div class="company-detail">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="company" class="content">
      <div class="header">
        <h1>{{ company.name }}</h1>
        <div class="meta">
          <span class="country">{{ company.country?.name }}</span>
          <span class="founded">Founded: {{ formatDate(company.date_founded) }}</span>
          <span class="status" :class="{ active: company.active }">
            {{ company.active ? 'Active' : 'Inactive' }}
          </span>
        </div>
      </div>

      <div class="description">
        <h2>About</h2>
        <p>{{ company.description }}</p>
      </div>

      <div class="employees" v-if="company.employees?.length">
        <h2>Employees ({{ company.employees.length }})</h2>
        <div class="employee-grid">
          <div v-for="employee in company.employees" :key="employee.id" class="employee-card">
            <h3>{{ employee.name }}</h3>
            <p class="job-title">{{ employee.job_title }}</p>
            <p class="contact">
              <a :href="'mailto:' + employee.email">{{ employee.email }}</a>
              <span v-if="employee.phone_number">{{ employee.phone_number }}</span>
            </p>
          </div>
        </div>
      </div>

      <div class="deals" v-if="company.deals?.length">
        <h2>Deals</h2>
        <div class="deals-list">
          <div v-for="deal in company.deals" :key="deal.id" class="deal-card">
            <div class="amount">£{{ formatAmount(deal.amount_raised) }}</div>
            <div class="date">{{ formatDate(deal.date_of_deal) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export default {
  name: 'CompanyDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      company: null,
      loading: true,
      error: null
    };
  },
  async created() {
    try {
      const response = await axios.get(`${API_BASE_URL}/companies/${this.id}/`);
      this.company = response.data;
    } catch (error) {
      this.error = 'Failed to load company details';
      console.error('Error loading company:', error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString();
    },
    formatAmount(amount) {
      return new Intl.NumberFormat('en-GB', {
        style: 'decimal',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(amount);
    }
  }
};
</script>

<style scoped>
.company-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: #dc3545;
}

.header {
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.meta {
  display: flex;
  gap: 1rem;
  color: #666;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background-color: #dc3545;
  color: white;
}

.status.active {
  background-color: #28a745;
}

.description {
  margin-bottom: 3rem;
}

.description h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.employee-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.employee-card {
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
}

.employee-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.job-title {
  color: #666;
  margin-bottom: 1rem;
}

.contact {
  font-size: 0.9rem;
}

.contact a {
  color: #007bff;
  text-decoration: none;
}

.contact span {
  display: block;
  color: #666;
}

.deals-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.deal-card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
}

.amount {
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
}

.date {
  color: #666;
  font-size: 0.9rem;
}
</style> 