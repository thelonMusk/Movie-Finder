import React, { useState } from 'react';
import { Search, Film, Star, Calendar, Clock, Sparkles } from 'lucide-react';
import './App.css';

export default function MovieFinder() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await fetch('http://localhost:5000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch results');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Failed to search. Make sure the Flask backend is running on port 5000.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="app-container">
      <div className="background-orb orb-1"></div>
      <div className="background-orb orb-2"></div>

      <div className="content-wrapper">
        <header className="header">
          <div className="header-content">
            <Film size={48} className="header-icon" />
            <h1 className="header-title">AI Movie Finder</h1>
          </div>
          <p className="header-subtitle">Powered by Groq AI - Describe what you want to watch</p>
        </header>

        <div className="search-container">
          <div className="search-glow"></div>
          <div className="search-box">
            <Sparkles size={24} className="search-icon" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="e.g., 'A mind-bending sci-fi thriller like Inception' or 'Cozy romantic comedy from the 90s'"
              className="search-input"
              disabled={loading}
            />
            <button
              onClick={handleSearch}
              disabled={loading || !query.trim()}
              className="search-button"
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  Searching...
                </>
              ) : (
                <>
                  <Search size={20} />
                  Find Movies
                </>
              )}
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {results?.analysis && (
          <div className="analysis-box">
            <div className="analysis-content">
              <Sparkles size={24} className="analysis-icon" />
              <div>
                <h3 className="analysis-title">AI Analysis</h3>
                <p className="analysis-text">{results.analysis}</p>
              </div>
            </div>
          </div>
        )}

        {results?.movies && results.movies.length > 0 && (
          <div className="movies-grid">
            {results.movies.map((movie, index) => (
              <div key={movie.imdbID || index} className="movie-card">
                <div className="movie-poster">
                  {movie.poster && movie.poster !== 'N/A' ? (
                    <img
                      src={movie.poster}
                      alt={movie.title}
                      className="poster-image"
                    />
                  ) : (
                    <div className="poster-placeholder">
                      <Film size={80} />
                    </div>
                  )}
                  
                  {movie.imdbRating && movie.imdbRating !== 'N/A' && (
                    <div className="rating-badge">
                      <Star size={16} fill="currentColor" />
                      {movie.imdbRating}
                    </div>
                  )}
                </div>

                <div className="movie-content">
                  <h3 className="movie-title">{movie.title}</h3>
                  
                  <div className="movie-meta">
                    {movie.year && (
                      <div className="meta-item">
                        <Calendar size={16} />
                        {movie.year}
                      </div>
                    )}
                    {movie.runtime && movie.runtime !== 'N/A' && (
                      <div className="meta-item">
                        <Clock size={16} />
                        {movie.runtime}
                      </div>
                    )}
                    {movie.language && movie.language !== 'N/A' && (
                      <div className="meta-item language-tag">
                        🌐 {movie.language.split(',')[0].trim()}
                      </div>
                    )}
                  </div>

                  {movie.genre && movie.genre !== 'N/A' && (
                    <div className="genre-tags">
                      {movie.genre.split(',').slice(0, 3).map((genre, i) => (
                        <span key={i} className="genre-tag">
                          {genre.trim()}
                        </span>
                      ))}
                    </div>
                  )}

                  {movie.plot && movie.plot !== 'N/A' && (
                    <p className="movie-plot">{movie.plot}</p>
                  )}

                  {movie.director && movie.director !== 'N/A' && (
                    <p className="movie-director">
                      <strong>Director:</strong> {movie.director}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {results && results.movies && results.movies.length === 0 && (
          <div className="no-results">
            <Film size={64} />
            <p>No movies found. Try a different search!</p>
          </div>
        )}
      </div>
    </div>
  );
}