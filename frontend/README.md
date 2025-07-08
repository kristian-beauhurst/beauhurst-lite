# Beauhurst Lite Frontend

A Vue.js frontend for the Beauhurst Lite application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run serve
```

The application will be available at `http://localhost:8080`.

## Features

- Real-time search with debouncing (triggers after 3 characters)
- Dynamic filter configuration from the backend
- Responsive grid layout for search results
- Company and employee icons for different result types
- Comprehensive filtering options:
  - Search type (All, Companies, Employees)
  - Date range
  - Deal amount range
  - Employee count range
  - Country selection
  - Sorting options

## Development

- The application uses Vue 3 with the Composition API
- Axios for API requests
- Font Awesome for icons
- CSS Grid and Flexbox for layouts
- Debounced search to prevent excessive API calls

## API Integration

The frontend integrates with the following backend endpoints:
- `GET /api/v1/search/config/filteroptions/` - Get filter configuration
- `GET /api/v1/search/` - Perform search with filters 