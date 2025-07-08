<template>
  <div class="employee-detail">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="employee" class="content">
      <div class="header">
        <h1>{{ employee.name }}</h1>
        <div class="meta">
          <span class="job-title">{{ employee.job_title }}</span>
          <span class="company" v-if="employee.company">
            <router-link :to="'/companies/' + employee.company.id">
              {{ employee.company.name }}
            </router-link>
          </span>
        </div>
      </div>

      <div class="contact">
        <h2>Contact Information</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <i class="fas fa-envelope"></i>
            <a :href="'mailto:' + employee.email">{{ employee.email }}</a>
          </div>
          <div class="contact-item" v-if="employee.phone_number">
            <i class="fas fa-phone"></i>
            <a :href="'tel:' + employee.phone_number">{{ employee.phone_number }}</a>
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
  name: 'EmployeeDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      employee: null,
      loading: true,
      error: null
    };
  },
  async created() {
    try {
      const response = await axios.get(`${API_BASE_URL}/employees/${this.id}/`);
      this.employee = response.data;
    } catch (error) {
      this.error = 'Failed to load employee details';
      console.error('Error loading employee:', error);
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.employee-detail {
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

.job-title {
  font-size: 1.2rem;
  color: #2c3e50;
}

.company a {
  color: #007bff;
  text-decoration: none;
}

.contact {
  margin-top: 3rem;
}

.contact h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
}

.contact-item i {
  color: #666;
  font-size: 1.2rem;
}

.contact-item a {
  color: #007bff;
  text-decoration: none;
}
</style> 