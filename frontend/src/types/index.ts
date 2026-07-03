export interface EmailMetadata {
  email_id: string;
  subject: string;
  summary: string;
  time: string;
  relevance: number;
  importance: number;
  is_starred: boolean;
  category: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  timestamp: string;
}

export interface EmailDetails extends EmailMetadata {
  body: string;
  deadline: string;
  tags: string[];
  labels: string[];
}

export interface CategoryCounts {
  [key: string]: number;
}

export interface AnalyticsData {
  top_interests: string[];
  top_tags: string[];
  emails_processed: number;
  labels_count: number;
  deadlines_count: number;
}
