import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import CompanyDetail from '@/components/CompanyDetail.vue'
import axios from 'axios'

jest.mock('axios')

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/companies/:id', component: CompanyDetail }
  ]
})

const mockCompanyData = {
  id: 1,
  name: 'Acme Corporation',
  description: 'A leading technology company specializing in innovative solutions.',
  date_founded: '2010-05-15',
  active: true,
  country: {
    id: 1,
    iso_code: 'GB',
    name: 'United Kingdom'
  },
  employees: [
    {
      id: 1,
      name: 'John Smith',
      job_title: 'Software Engineer',
      email: 'john.smith@acme.com',
      phone_number: '+44 123 456 7890'
    },
    {
      id: 2,
      name: 'Jane Doe',
      job_title: 'Product Manager',
      email: 'jane.doe@acme.com',
      phone_number: '+44 123 456 7891'
    }
  ],
  deals: [
    {
      id: 1,
      amount_raised: 1000000,
      date_of_deal: '2023-01-15'
    },
    {
      id: 2,
      amount_raised: 2500000,
      date_of_deal: '2023-06-20'
    }
  ]
}

describe('CompanyDetail.vue', () => {
  let wrapper

  beforeEach(() => {
    axios.get.mockClear()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })

  it('renders loading state correctly', async () => {
    axios.get.mockImplementation(() => new Promise(() => {}))

    wrapper = mount(CompanyDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders error state correctly', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network error'))

    wrapper = mount(CompanyDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders company data correctly', async () => {
    axios.get.mockResolvedValueOnce({ data: mockCompanyData })

    wrapper = mount(CompanyDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders company without employees correctly', async () => {
    const companyWithoutEmployees = {
      ...mockCompanyData,
      employees: []
    }
    axios.get.mockResolvedValueOnce({ data: companyWithoutEmployees })

    wrapper = mount(CompanyDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders company without deals correctly', async () => {
    const companyWithoutDeals = {
      ...mockCompanyData,
      deals: []
    }
    axios.get.mockResolvedValueOnce({ data: companyWithoutDeals })

    wrapper = mount(CompanyDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })

  it('renders inactive company correctly', async () => {
    const inactiveCompany = {
      ...mockCompanyData,
      active: false
    }
    axios.get.mockResolvedValueOnce({ data: inactiveCompany })

    wrapper = mount(CompanyDetail, {
      props: { id: 1 },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.html()).toMatchSnapshot()
  })
}) 