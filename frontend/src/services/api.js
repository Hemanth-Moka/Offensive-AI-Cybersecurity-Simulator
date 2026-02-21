import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Password Simulator API
export const passwordAPI = {
  analyze: (data) => api.post('/api/password/analyze', data),
  crackHash: (data) => api.post('/api/password/crack-hash', data),
  getHistory: (limit = 50) => api.get(`/api/password/history?limit=${limit}`),
  getStats: () => api.get('/api/password/stats'),
}

// Phishing Simulator API
export const phishingAPI = {
  analyze: (data) => api.post('/api/phishing/analyze', data),
  simulateCampaign: (data) => api.post('/api/phishing/campaign', data),
  getHistory: (limit = 50) => api.get(`/api/phishing/history?limit=${limit}`),
  getStats: () => api.get('/api/phishing/stats'),
}

// Vishing (Voice Phishing) Simulator API
export const vishingAPI = {
  analyze: (data) => api.post('/api/vishing/analyze', data),
  simulateCampaign: (data) => api.post('/api/vishing/campaign', data),
  getHistory: (limit = 50) => api.get(`/api/vishing/history?limit=${limit}`),
  getStats: () => api.get('/api/vishing/stats'),
}

export default api
