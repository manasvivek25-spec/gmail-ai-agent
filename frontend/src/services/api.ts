import axios from 'axios';

const API_BASE = 'https://gmail-ai-agent-ih4e.onrender.com/api';

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  getEmails: () => axios.get(`${API_BASE}/emails`),
  getEmailDetails: (id: string) => axios.get(`${API_BASE}/emails/${id}`),
  getRawEmail: (id: string) => axios.get(`${API_BASE}/emails/${id}/raw`),
  getDeadlines: () => axios.get(`${API_BASE}/deadlines`),
  getRecommended: () => axios.get(`${API_BASE}/recommended`),
  getCategories: () => axios.get(`${API_BASE}/categories`),
  getAnalytics: () => axios.get(`${API_BASE}/analytics`),
  getCategoryEmails: (name: string) => axios.get(`${API_BASE}/categories/${name}`),
  getLabels: () => axios.get(`${API_BASE}/labels`),
  getLabelEmails: (name: string) => axios.get(`${API_BASE}/labels/${name}`),
  getStarred: () => axios.get(`${API_BASE}/starred`),
  toggleBookmark: (id: string) => axios.post(`${API_BASE}/toggle-bookmark/${id}`),
  search: (query: string) => axios.post(`${API_BASE}/search`, { query }),
  ask: (query: string) => axios.post(`${API_BASE}/ask`, { query }),
  refresh: () => axios.post(`${API_BASE}/refresh`),
};
