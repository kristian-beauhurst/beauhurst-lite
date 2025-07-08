<template>
  <main class="main">
    <div class="search-container">
      <div class="search-bar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search companies and employees..."
          @input="handleSearch"
          class="search-input"
        />
      </div>

      <div class="filters" v-if="filterConfig">
        <!-- Search Type -->
        <div class="filter-group">
          <h3>{{ filterConfig.type.label }}</h3>
          <div class="checkbox-group">
            <label v-for="option in filterConfig.type.options" :key="option.value">
              <input
                type="checkbox"
                :value="option.value"
                v-model="selectedTypes"
                @change="handleSearch"
              />
              {{ option.label }}
            </label>
          </div>
        </div>

        <!-- Date Range -->
        <div class="filter-group">
          <h3>{{ filterConfig.date_range.label }}</h3>
          <div class="date-range">
            <input
              type="date"
              v-model="dateFrom"
              @change="handleSearch"
              :placeholder="filterConfig.date_range.fields[0].placeholder"
            />
            <input
              type="date"
              v-model="dateTo"
              @change="handleSearch"
              :placeholder="filterConfig.date_range.fields[1].placeholder"
            />
          </div>
        </div>

        <!-- Deal Amount -->
        <div class="filter-group">
          <h3>{{ filterConfig.deal_amount.label }}</h3>
          <div class="number-range">
            <input
              type="number"
              v-model="dealAmountMin"
              @change="handleSearch"
              :placeholder="filterConfig.deal_amount.fields[0].placeholder"
            />
            <input
              type="number"
              v-model="dealAmountMax"
              @change="handleSearch"
              :placeholder="filterConfig.deal_amount.fields[1].placeholder"
            />
          </div>
        </div>

        <!-- Employee Count -->
        <div class="filter-group">
          <h3>{{ filterConfig.employee_count.label }}</h3>
          <div class="number-range">
            <input
              type="number"
              v-model="employeeCountMin"
              @change="handleSearch"
              :placeholder="filterConfig.employee_count.fields[0].placeholder"
            />
            <input
              type="number"
              v-model="employeeCountMax"
              @change="handleSearch"
              :placeholder="filterConfig.employee_count.fields[1].placeholder"
            />
          </div>
        </div>

        <!-- Countries -->
        <div class="filter-group">
          <h3>{{ filterConfig.country.label }}</h3>
          <select
            multiple
            v-model="selectedCountries"
            @change="handleSearch"
            class="country-select"
          >
            <option
              v-for="option in filterConfig.country.options"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>

        <!-- Sort -->
        <div class="filter-group">
          <h3>{{ filterConfig.sort.label }}</h3>
          <div class="sort-controls">
            <select v-model="sortBy" @change="handleSearch">
              <option
                v-for="option in filterConfig.sort.options"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
            <select v-model="sortOrder" @change="handleSearch">
              <option
                v-for="option in filterConfig.sort.order.options"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div class="results" v-if="searchResults.sections">
      <div v-for="section in searchResults.sections" :key="section.title" class="result-section">
        <h2>{{ section.title }} ({{ section.count }})</h2>
        <div class="result-grid">
          <router-link
            v-for="result in section.results"
            :key="result.id"
            :to="'/' + (section.title === 'Companies' ? 'companies' : 'employees') + '/' + result.id"
            class="result-card"
          >
            <div class="result-icon">
              <i :class="section.title === 'Companies' ? 'fas fa-building' : 'fas fa-user'"></i>
            </div>
            <div class="result-content">
              <h3>{{ result.title }}</h3>
              <p>{{ result.subtitle }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios';
import debounce from 'debounce';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export default {
  name: 'SearchInterface',
  data() {
    return {
      searchQuery: '',
      filterConfig: null,
      searchResults: { sections: [] },
      selectedTypes: ['all'],
      dateFrom: '',
      dateTo: '',
      dealAmountMin: '',
      dealAmountMax: '',
      employeeCountMin: '',
      employeeCountMax: '',
      selectedCountries: [],
      sortBy: '',
      sortOrder: 'desc'
    };
  },
  async created() {
    try {
      const response = await axios.get(`${API_BASE_URL}/search/config/filteroptions/`);
      this.filterConfig = response.data;
      
      // Restore state from URL parameters
      const query = this.$route.query;
      if (query.q) this.searchQuery = query.q;
      if (query.type) this.selectedTypes = query.type.split(',');
      if (query.date_from) this.dateFrom = query.date_from;
      if (query.date_to) this.dateTo = query.date_to;
      if (query.deal_amount_min) this.dealAmountMin = query.deal_amount_min;
      if (query.deal_amount_max) this.dealAmountMax = query.deal_amount_max;
      if (query.employee_count_min) this.employeeCountMin = query.employee_count_min;
      if (query.employee_count_max) this.employeeCountMax = query.employee_count_max;
      if (query.country) this.selectedCountries = Array.isArray(query.country) ? query.country : [query.country];
      if (query.sort_by) this.sortBy = query.sort_by;
      if (query.sort_order) this.sortOrder = query.sort_order;

      // If we have a search query, perform the search
      if (this.searchQuery) {
        this.handleSearch();
      }
    } catch (error) {
      console.error('Error loading filter configuration:', error);
    }
  },
  methods: {
    handleSearch: debounce(async function() {
      if (this.searchQuery.length < 3) {
        this.searchResults = { sections: [] };
        return;
      }

      try {
        const params = {
          q: this.searchQuery,
          type: this.selectedTypes.join(','),
          date_from: this.dateFrom,
          date_to: this.dateTo,
          deal_amount_min: this.dealAmountMin,
          deal_amount_max: this.dealAmountMax,
          employee_count_min: this.employeeCountMin,
          employee_count_max: this.employeeCountMax,
          country: this.selectedCountries,
          sort_by: this.sortBy,
          sort_order: this.sortOrder
        };

        // Update URL with current search parameters
        this.$router.replace({
          query: {
            ...params,
            country: this.selectedCountries.length > 0 ? this.selectedCountries : undefined
          }
        });

        const response = await axios.get(`${API_BASE_URL}/search/`, { params });
        console.log('Search response:', response.data);
        this.searchResults = response.data;
      } catch (error) {
        console.error('Error performing search:', error);
      }
    }, 300)
  },
  watch: {
    // Watch for changes in route query parameters
    '$route.query': {
      handler(newQuery) {
        // Only update if the query parameters have actually changed
        if (JSON.stringify(newQuery) !== JSON.stringify(this.$route.query)) {
          this.handleSearch();
        }
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.search-container {
  margin-bottom: 2rem;
}

.search-bar {
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1.1rem;
  border: 2px solid #ddd;
  border-radius: 4px;
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.filter-group {
  margin-bottom: 1rem;
}

.filter-group h3 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
  color: #2c3e50;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-range,
.number-range {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

input[type="date"],
input[type="number"],
select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.country-select {
  height: 120px;
}

.sort-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.result-section {
  margin-bottom: 2rem;
}

.result-section h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.result-card {
  text-decoration: none;
  color: inherit;
  display: block;
  transition: transform 0.2s;
}

.result-card:hover {
  transform: translateY(-2px);
}

.result-icon {
  font-size: 2rem;
  color: #2c3e50;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 50%;
}

.result-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.result-content p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}
</style> 