<template>
  <div class="app">
    <header class="header">
      <h1>Beauhurst Junior</h1>
    </header>
    
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
@import '@fortawesome/fontawesome-free/css/all.css';

.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
}

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