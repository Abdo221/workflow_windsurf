interface NewsItem {
  id: string;
  title: string;
  description: string;
  url: string;
  source_name: string;
  published_at: string;
  fetched_at: string;
}

interface NewsResponse {
  status: 'FRESH' | 'CACHED' | 'PARTIAL';
  attempts: number;
  category: string;
  items: NewsItem[];
}

export const fetchNews = async (category: string): Promise<NewsResponse> => {
  const response = await fetch('/api/news/fetch', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ category }),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch news');
  }

  return response.json();
};

export type { NewsItem, NewsResponse };
