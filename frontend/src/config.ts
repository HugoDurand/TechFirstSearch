function getApiBaseUrl(): string {
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }
    
    if (hostname === 'techfirstsearch.com' || hostname.includes('techfirstsearch')) {
      return 'https://techfirstsearch-production.up.railway.app';
    }
    
    if (hostname.includes('railway.app')) {
      return 'https://techfirstsearch-production.up.railway.app';
    }
  }
  
  return process.env.EXPO_PUBLIC_API_BASE_URL || 'http://localhost:8000';
}

export const API_BASE_URL = getApiBaseUrl();

export const ENDPOINTS = {
  FEED: `${API_BASE_URL}/api/feed`,
  SEARCH: `${API_BASE_URL}/api/search`,
  ARTICLE: (id: number) => `${API_BASE_URL}/api/article/${id}`,
  HEALTH: `${API_BASE_URL}/api/health`,
};

export const CONTENT_TYPE_COLORS = {
  paper: '#3B82F6',
  research: '#8B5CF6',
  news: '#EF4444',
  tutorial: '#10B981',
  essay: '#F59E0B',
  article: '#6366F1',
  post: '#EC4899',
};

