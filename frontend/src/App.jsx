import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import ProfileHeader from './components/ProfileHeader';
import StatsGrid from './components/StatsGrid';
import PostsGrid from './components/PostsGrid';
import HashtagsList from './components/HashtagsList';
import KeywordsList from './components/KeywordsList';
import PostingSchedule from './components/PostingSchedule';

function App() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (username) => {
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/analyze/${username}`);
      if (!response.ok) {
        throw new Error('Profile not found');
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center py-10 px-4">
      <h1 className="text-4xl font-bold mb-8 text-dark tracking-tight">
        Instagram <span className="text-primary">Profile Analyzer</span>
      </h1>

      <div className="w-full max-w-2xl mb-12">
        <SearchBar onSearch={handleSearch} loading={loading} />
      </div>

      {error && (
        <div className="text-red-500 mb-8 font-medium bg-red-50 px-4 py-2 rounded-lg">
          {error}
        </div>
      )}

      {data && (
        <div className="w-full max-w-5xl space-y-8 animate-fade-in-up">
          <ProfileHeader profile={data} />
          <StatsGrid stats={data} />

          <div className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-2">
              {data.recent_posts && data.recent_posts.length > 0 && (
                <PostsGrid posts={data.recent_posts} />
              )}
              {/* Hashtags and Keywords */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <HashtagsList hashtags={data.top_hashtags} />
                <KeywordsList keywords={data.top_keywords} />
              </div>

              {/* Posting Schedule */}
              <div className="mb-8">
                <PostingSchedule schedule={data.posting_schedule} />
              </div>
            </div>
            {/* The third column is now empty or can be used for other content */}
            <div>
              {/* This div was previously for HashtagsList, now it's moved */}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
