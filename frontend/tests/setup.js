import { config } from '@vue/test-utils'

// Global test configuration
config.global.mocks = {
  // Mock router
  $router: {
    push: jest.fn(),
    replace: jest.fn(),
    go: jest.fn(),
    back: jest.fn(),
    forward: jest.fn()
  },
  // Mock route
  $route: {
    params: {},
    query: {},
    path: '/'
  }
}

// Mock axios globally
jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn()
})) 