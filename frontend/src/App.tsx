import { useState } from 'react';
import { fetchNews, NewsItem, NewsResponse } from './api';
import './App.css';

function App() {
  const [category, setCategory] = useState('');
  const [items, setItems] = useState<NewsItem[]>([]);
  const [status, setStatus] = useState<'FRESH' | 'CACHED' | 'PARTIAL' | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetch = async () => {
    if (!category.trim()) return;

    setLoading(true);
    setError(null);
    setItems([]);
    setStatus(null);

    try {
      const response: NewsResponse = await fetchNews(category.trim());
      setItems(response.items);
      setStatus(response.status);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="container">
      <h1>News Fetcher</h1>
      
      <div className="input-group">
        <input
          type="text"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          placeholder="Enter category (e.g., science, sports)"
          onKeyPress={(e) => e.key === 'Enter' && handleFetch()}
          disabled={loading}
        />
        <button onClick={handleFetch} disabled={loading || !category.trim()}>
          {loading ? 'Fetching...' : 'Fetch'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {status && (
        <div className={`status ${status.toLowerCase()}`}>
          Status: {status} ({items.length} items)
        </div>
      )}

      {items.length > 0 && (
        <ul className="news-list">
          {items.map((item) => (
            <li key={item.id} className="news-item">
              <h3>
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.title}
                </a>
              </h3>
              <p>{item.description}</p>
              <div className="meta">
                Source: {item.source_name} | Published: {formatDate(item.published_at)}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
