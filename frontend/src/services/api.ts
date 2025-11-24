import axios from 'axios';
import { ENDPOINTS } from '../config';
import { FeedResponse, SearchResponse, ContentDetail } from '../types';

const api = axios.create({
  timeout: 10000,
});

export const fetchFeed = async (limit = 50, offset = 0): Promise<FeedResponse> => {
  const response = await api.get(ENDPOINTS.FEED, {
    params: { limit, offset },
  });
  return response.data;
};

export const searchContent = async (query: string, limit = 50): Promise<SearchResponse> => {
  const response = await api.get(ENDPOINTS.SEARCH, {
    params: { q: query, limit },
  });
  return response.data;
};

export const fetchArticle = async (id: number): Promise<ContentDetail> => {
  const response = await api.get(ENDPOINTS.ARTICLE(id));
  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get(ENDPOINTS.HEALTH);
  return response.data;
};

