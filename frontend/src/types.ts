export interface Content {
  id: number;
  title: string;
  url: string;
  source_name: string;
  content_type: string;
  published_date: string;
  thumbnail_url?: string;
  author?: string;
  tags?: string[];
  fetched_date: string;
  created_at: string;
  ai_summary?: string;
}

export interface ContentDetail extends Content {
  reader_mode_content?: string;
  full_content?: string;
  ai_key_points?: string[];
}

export interface FeedResponse {
  total: number;
  items: Content[];
}

export interface SearchResponse {
  total: number;
  items: Content[];
}
