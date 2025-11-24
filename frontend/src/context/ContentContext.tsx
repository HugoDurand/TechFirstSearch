import React, { createContext, useState, useContext, ReactNode } from 'react';
import { Content, FeedResponse } from '../types';
import { fetchFeed, searchContent } from '../services/api';

interface ContentContextType {
  contents: Content[];
  loading: boolean;
  error: string | null;
  total: number;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  loadFeed: () => Promise<void>;
  loadMore: () => Promise<void>;
  search: (query: string) => Promise<void>;
  refresh: () => Promise<void>;
}

const ContentContext = createContext<ContentContextType | undefined>(undefined);

export const ContentProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [contents, setContents] = useState<Content[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');

  const loadFeed = async () => {
    if (loading) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await fetchFeed(50, 0);
      setContents(data.items);
      setTotal(data.total);
      setOffset(50);
    } catch (err) {
      setError('Failed to load feed');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadMore = async () => {
    if (loading || searchQuery) return;
    
    setLoading(true);
    
    try {
      const data = await fetchFeed(50, offset);
      setContents([...contents, ...data.items]);
      setOffset(offset + 50);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const search = async (query: string) => {
    if (!query.trim()) {
      loadFeed();
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await searchContent(query);
      setContents(data.items);
      setTotal(data.total);
    } catch (err) {
      setError('Search failed');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const refresh = async () => {
    setOffset(0);
    if (searchQuery) {
      await search(searchQuery);
    } else {
      await loadFeed();
    }
  };

  return (
    <ContentContext.Provider
      value={{
        contents,
        loading,
        error,
        total,
        searchQuery,
        setSearchQuery,
        loadFeed,
        loadMore,
        search,
        refresh,
      }}
    >
      {children}
    </ContentContext.Provider>
  );
};

export const useContent = () => {
  const context = useContext(ContentContext);
  if (context === undefined) {
    throw new Error('useContent must be used within a ContentProvider');
  }
  return context;
};

