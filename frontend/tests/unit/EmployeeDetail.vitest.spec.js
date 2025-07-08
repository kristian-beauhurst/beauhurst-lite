import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import EmployeeDetail from '@/components/EmployeeDetail.vue'
import axios from 'axios'
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'

vi.mock('axios')

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/employees/:id', component: EmployeeDetail }
  ]
})

const mockEmployeeData = {
  id: 1,
  name: 'John Smith',
  job_title: 'Senior Software Engineer',
  email: 'john.smith@acme.com',
  phone_number: '+44 123 456 7890',
  gender: 'M',
  company: {
    id: 1,
    name: 'Acme Corporation'
  }
}

const mockEmployeeWithoutPhone = {
  id: 2,
  name: 'Jane Doe',
  job_title: 'Product Manager',
  email: 'jane.doe@acme.com',
  phone_number: null,
  gender: 'F',
  company: {
    id: 1,
    name: 'Acme Corporation'
  }
}

describe('EmployeeDetail.vue (Vitest)', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })

  it('renders loading state correctly', async () => {
    axios.get.mockImplementation(() => new Promise(() => {}))

    wrapper = mount(EmployeeDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders error state correctly', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network error'))

    wrapper = mount(EmployeeDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders employee data correctly', async () => {
    axios.get.mockResolvedValueOnce({ data: mockEmployeeData })

    wrapper = mount(EmployeeDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders employee without phone number correctly', async () => {
    axios.get.mockResolvedValueOnce({ data: mockEmployeeWithoutPhone })

    wrapper = mount(EmployeeDetail, {
      props: { id: 2 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders employee without company correctly', async () => {
    const employeeWithoutCompany = {
      ...mockEmployeeData,
      company: null
    }
    axios.get.mockResolvedValueOnce({ data: employeeWithoutCompany })

    wrapper = mount(EmployeeDetail, {
      props: { id: 3 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })
}) 