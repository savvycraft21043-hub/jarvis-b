import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

export const runPipeline = () => api.post('/api/pipeline/run').then((r) => r.data)
export const fetchSignals = () => api.get('/api/signals').then((r) => r.data)
export const fetchOpportunities = () => api.get('/api/opportunities').then((r) => r.data)
export const search = (q) => api.get('/api/search', { params: { q } }).then((r) => r.data)
export const fetchCompanies = () => api.get('/api/companies').then((r) => r.data)
export const fetchCompany = (id) => api.get(`/api/companies/${id}`).then((r) => r.data)
export const fetchGraph = () => api.get('/api/graph').then((r) => r.data)
